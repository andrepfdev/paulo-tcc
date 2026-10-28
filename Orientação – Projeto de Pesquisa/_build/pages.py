import json,subprocess,sys,re
pdf=sys.argv[1]
n=int(re.search(r'Pages:\s+(\d+)',subprocess.run(['pdfinfo',pdf],capture_output=True,text=True).stdout).group(1))
keys=json.load(open('toc_keys.json'))
texts=[subprocess.run(['pdftotext','-f',str(p),'-l',str(p),'-layout',pdf,'-'],capture_output=True,text=True).stdout for p in range(1,n+1)]
norm=lambda s: re.sub(r'\s+',' ',s).strip().upper()
res={}
last=0
sumario_page=None
for p,t in enumerate(texts,1):
    if 'SUMÁRIO' in t and sumario_page is None: sumario_page=p
for k in keys:
    num,title,level=k['num'],k['title'].replace('*',''),k['level']
    target=norm((num+' ' if num else '')+title)[:45]
    for p in range(max(sumario_page+1,last),n+1):
        lines=[norm(l) for l in texts[p-1].splitlines()]
        if any(l.startswith(target) for l in lines):
            res[k['key']]=p-1; last=p; break
    else: print('NOT FOUND',k['key'])
first=min(res.values())+1
res['__start']=first-1
json.dump(res,open('pages.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1)); print('sumario pdf page',sumario_page)
