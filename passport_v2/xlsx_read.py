"""Minimal stdlib .xlsx reader: read(path) -> {sheet name: [[cell, ...], ...]}."""
import re,html,sys,zipfile,json
def col2n(c):
    n=0
    for ch in c: n=n*26+ord(ch)-64
    return n-1
def read(path):
    z=zipfile.ZipFile(path)
    strs=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        ss=z.read('xl/sharedStrings.xml').decode()
        strs=[html.unescape(''.join(re.findall(r'<t[^>]*>(.*?)</t>',m,re.S))) for m in re.findall(r'<si>(.*?)</si>',ss,re.S)]
    wb=z.read('xl/workbook.xml').decode()
    rels=z.read('xl/_rels/workbook.xml.rels').decode()
    relmap=dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"',rels)); relmap.update({b:a for a,b in re.findall(r'Target="([^"]+)"[^>]*Id="([^"]+)"',rels)})
    out={}
    for name,rid in re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"',wb):
        tgt=relmap[rid].lstrip('/'); tgt=tgt if tgt.startswith('xl/') else 'xl/'+tgt
        s=z.read(tgt).decode(); rows=[]
        for row in re.findall(r'<row[^>]*>(.*?)</row>',s,re.S):
            vals={}
            for attrs,body in re.findall(r'<c ([^>]*?)(?:/>|>(.*?)</c>)',row,re.S):
                ref=re.search(r'r="([A-Z]+)',attrs).group(1); t=re.search(r'\bt="(\w+)"',attrs)
                v=re.search(r'<v>(.*?)</v>',body or '',re.S)
                if t and t.group(1)=='inlineStr': val=html.unescape(''.join(re.findall(r'<t[^>]*>(.*?)</t>',body,re.S)))
                elif not v: continue
                elif t and t.group(1)=='s': val=strs[int(v.group(1))]
                else: val=html.unescape(v.group(1))
                vals[col2n(ref)]=val
            if vals: rows.append([vals.get(i,'') for i in range(max(vals)+1)])
        out[html.unescape(name)]=rows
    return out
if __name__=='__main__':
    d=read(sys.argv[1])
    for k,rows in d.items():
        print('==',k,'rows:',len(rows))
        for r in rows[:int(sys.argv[2]) if len(sys.argv)>2 else 1]: print(r)
