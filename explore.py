#!/usr/bin/python3
import clconvert
import codegen
import cpsconvert
import itertools
import re
import string2ast
import symbol

def py2clj(s):
    s0 = str(s)
    s1 = re.sub(r'\[', '(', s0)
    s2 = re.sub(r']', ')', s1)
    s3 = re.sub(r'\'', '', s2)
    s4 = re.sub(r',', '', s3)
    return s4

colorList = itertools.cycle(['red', 'green', 'blue', 'black', 'darkgreen', 'purple'])

css = '''
<style>
div.row {
    page-break-after: always;
    display: flex;
}

div.col {
    flex: 10%;
    border-left: 1px dotted black;
    margin-left:20px;
}
div .lisp {
    border-top: 1px dotted;
    border-left: 1px dotted;
    margin-left:5px;
    padding-left:5px;
    /*opacity: 0.9;*/
}
div .bracket {
    margin-bottom:2px;
}
</style>
'''

def scheme2html(s):
    i = 0
    output=[]
    for c in s:
        if c == '(':
            color = next(colorList)
            output.append(f'<div class="bracket">(<div style="border-color:{color}" class="lisp">')
            continue
        if c == ')':
            output.append('</div>)</div>')
            continue
        output.append(c)
    return str.join('', output)


schemes = [
        '''10''',
        '''
        (define x 10)
        x
        ''',
        '''
        (define func (lambda (x) x))
        (func 20)''',
        '''
        (define func (lambda (x) (lambda (y) (+ x y))))
        (func 20)'''
        ]

with open('report.html', 'w') as report:
    report.write(f'<html>{css}<body>')
    for s in schemes:
        symbol.varNumber = 0
        a = string2ast.parse(s)
        b = cpsconvert.cpsConvert(a)
        c = clconvert.closureConvert(b)
        code = codegen.codeGenerateDebug(c)

        report.write(s)
        report.write('<div class="row">')
        report.write('<div class="col">')
        report.write(scheme2html(py2clj(debug.source(b))))
        report.write('</div>')
        report.write('<div class="col">')
        report.write(scheme2html(py2clj(debug.source(c))))
        report.write('</div>')
        report.write('<div class="col">')
        report.write('<pre>')
        report.write(str(code))
        report.write('</pre>')
        report.write('</div>')
        report.write('</div>')
        report.write('<hr>')

        print(f'INPUT  = {py2clj(debug.source(a))}')
        print(f'')
        print(f'CPS    = {py2clj(debug.source(b))}')
        print(f'')
        print(f'CLCONV = {py2clj(debug.source(c))}')
        print(f'HTML = {scheme2html(py2clj(debug.source(c)))}')
    report.write('</body></html>')
