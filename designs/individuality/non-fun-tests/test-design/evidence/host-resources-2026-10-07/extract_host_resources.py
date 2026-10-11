"""Derive host CPU/RAM and collator/driver resource timelines from saved claim-run evidence.

Run: python3 extract_host_resources.py <path to coinage-evidence/claims-capacity-2026-10-01>
The raw evidence is kept locally, not on this site. Writes host-resources.raw.json in the current directory.
"""
import json,re,datetime,sys,math
root=sys.argv[1]
def iso(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
out={}
for run,label in [('36832069153','20,000 claims'),('36836204912','40,000 claims'),('36840043405','100,000 claims')]:
    p=f'{root}/{run}/original'
    s=json.load(open(p+'/claim-burst-summary.json')); fx=json.load(open(p+'/claim-burst-fixture.json'))
    t0=iso(s['wallStart'])
    rows=[json.loads(l) for l in open(p+'/node-metrics.jsonl')]
    starts={}
    for n,d in rows[0]['nodes'].items():
        for m in d.get('metrics',[]):
            if m.startswith('substrate_process_start_time_seconds'): starts[n]=float(m.rsplit(' ',1)[1])
    host=[];last=None;lastc={}
    for r in rows:
        h=r.get('host',{});st=h.get('/proc/stat','');mem=h.get('/proc/meminfo','')
        if not (isinstance(st,str) and st and isinstance(mem,str)): continue
        cpu=list(map(int,st.splitlines()[0].split()[1:9]));tot=sum(cpu);idle=cpu[3]+cpu[4]
        cores={}
        for line in st.splitlines()[1:]:
            f=line.split()
            if f and re.fullmatch(r'cpu\d+',f[0]):
                v=list(map(int,f[1:9]));ct=sum(v);ci=v[3]+v[4];pv=lastc.get(f[0])
                if pv and ct>pv[0]: cores[f[0]]=100*(1-(ci-pv[1])/(ct-pv[0]))
                lastc[f[0]]=(ct,ci)
        vals={k:int(v) for k,v in re.findall(r'^(\w+):\s+(\d+)',mem,re.M)}
        if last and tot>last[0]:
            host.append({'t':round(r['time']-t0,1),'busy':round(100*(1-(idle-last[1])/(tot-last[0])),2),
                         'maxCore':round(max(cores.values()),1) if cores else None,
                         'usedGiB':round((vals['MemTotal']-vals['MemAvailable'])/2**20,3),'totalGiB':round(vals['MemTotal']/2**20,1)})
        last=(tot,idle)
    # process RSS from ps snapshots; omni-node PIDs map to collators in start order
    snaps=[];cur=None
    for line in open(p+'/process-samples.txt'):
        if 'UTC 2026' in line:
            ts=datetime.datetime.strptime(line.strip(),'%a %b %d %H:%M:%S UTC %Y').replace(tzinfo=datetime.timezone.utc).timestamp()
            cur={'t':ts,'procs':[]};snaps.append(cur);continue
        f=line.split()
        if cur and len(f)>=5 and f[0].isdigit(): cur['procs'].append((int(f[0]),float(f[2]),int(f[3]),' '.join(f[4:])))
    omni=sorted({pid for sn in snaps for pid,_,_,c in sn['procs'] if c.startswith('polkadot-omni')})
    order=sorted([n for n in starts if n.startswith('Collator')],key=lambda n:starts[n])
    names=dict(zip(omni,order))
    driver_pids={pid for sn in snaps for pid,_,rss,c in sn['procs'] if c=='MainThread' and rss>500000}
    procs=[]
    for sn in snaps:
        row={'t':round(sn['t']-t0,1)}
        for pid,pc,rss,c in sn['procs']:
            if names.get(pid) in ('Collator-1502','Collator-1502-2'): row[names[pid]]=round(rss/2**20,3)
            if pid in driver_pids: row['driver']=round(rss/2**20,3)
        procs.append(row)
    # average cores per process over windows, from ps lifetime %CPU and known start times
    def cputime(sn,pid,start): 
        for q,pc,_,_ in sn['procs']:
            if q==pid: return pc/100*(sn['t']-start)
    def window_cores(a,b):
        sa=min(snaps,key=lambda x:abs(x['t']-(t0+a)));sb=min(snaps,key=lambda x:abs(x['t']-(t0+b)))
        res={}
        for pid,n in names.items():
            if n in ('Collator-1502','Collator-1502-2'):
                ca,cb=cputime(sa,pid,starts[n]),cputime(sb,pid,starts[n])
                if ca is not None and cb is not None: res[n]=round((cb-ca)/(sb['t']-sa['t']),2)
        for pid in driver_pids:
            first=min(x['t'] for x in snaps if any(q==pid for q,_,_,_ in x['procs']))
            ca,cb=cputime(sa,pid,first),cputime(sb,pid,first)
            if ca is not None and cb is not None: res['driver']=round((cb-ca)/(sb['t']-sa['t']),2)
        return res,round(sa['t']-t0),round(sb['t']-t0)
    prep=fx['preparationMs']/1e3; settled=s['settledAtMs']/1e3
    win={'beforeFixtures':window_cores(-prep-240,-prep-30),'fixtures':window_cores(-prep+60,-60),'burst':window_cores(0,settled)}
    out[label]={'run':int(run),'burstStartUtc':s['wallStart'],'fixturePreparationSeconds':round(prep,3),
        'lastReceiptSeconds':round(settled,3),'stageSeconds':round(s['elapsedMs']/1e3,3),
        'networkStartSeconds':round(min(starts.values())-t0,1),
        'host':host,'processRssGiB':procs,'collatorAverageCores':win,
        'pidMapping':{str(k):v for k,v in names.items()},'driverPids':sorted(driver_pids)}
    def phase(a,b,key):
        v=[x[key] for x in host if a<=x['t']<=b and x[key] is not None]; return (round(min(v),1),round(sum(v)/len(v),1),round(max(v),1)) if v else None
    print(label,'netStart',out[label]['networkStartSeconds'],'prep',round(prep),'settled',round(settled))
    print('  busy min/avg/max  idle-before-fixtures',phase(-prep-240,-prep-30,'busy'),' fixtures',phase(-prep+60,-60,'busy'),' burst',phase(0,settled,'busy'),' after',phase(settled+30,settled+600,'busy'))
    print('  maxCore burst',phase(0,settled,'maxCore'),' fixtures',phase(-prep+60,-60,'maxCore'))
    print('  total',host[0]['totalGiB']);print('  usedGiB idle',phase(-prep-240,-prep-30,'usedGiB'),' fixtures',phase(-prep+60,-60,'usedGiB'),' burst',phase(0,settled,'usedGiB'))
    def rss(a,b,k):
        v=[x[k] for x in procs if a<=x['t']<=b and k in x]; return (round(min(v),2),round(max(v),2)) if v else None
    for k in ['Collator-1502','Collator-1502-2','driver']: print('  rss',k,'idle',rss(-prep-240,-prep-30,k),'fixtures',rss(-prep+60,-60,k),'burst',rss(0,settled,k))
    print('  cores',win, 'pidmap',names,'driver',driver_pids)
json.dump(out,open('host-resources.raw.json','w'),indent=1)
