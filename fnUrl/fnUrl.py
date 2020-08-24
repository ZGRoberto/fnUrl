"""
Script para ler arquivo com URLs em arquivo txt e
 gerar arquuivo com linhas comando em Fortigate 100F para liberação no firewall.
O script e o arquivo txt devem estar no mesmo diretorio.
Autor: Roberto Gaebler Zoccoli
Sintaxe: Bruno Nunes Barbosa
"""
import re, os, sys
def tryTxt(P, urlArq):
    tentar = True
    while tentar:
        tentar = False
        try:
            temp = open(P+"\\"+urlArq+'.txt')
            temp.close()
        except:
            tentar = True
            print('Arquivo não encontrado: %s.txt \n' %(urlArq))
            urlArq = input('Informe nome do arquivo de URLs(.txt) ou "PARE": ')
        if "PARE" in urlArq.upper():
           sys.exit()
    return urlArq
def lerTxt(P, urlArq):
    arqEnt = {}
    temp = open(P+"\\"+urlArq+'.txt', 'r', encoding="utf8")
    E = 0
    for reg in temp:
        reg = re.sub('\n', '', reg)
        arqEnt[E] = reg
        E += 1
    temp.close()
    return arqEnt, E
def gravaTxt(P, urlArq, E, arqEnt):
    temp = open(P+"\\"+urlArq+"-cmd.txt", 'w')
    S = 0
    temp.write('config webfilter urlfilter\n')
    temp.write('\tedit 1\n')
    temp.write('\t\tset name "Auto-webfilter-urlfilter_z0a1vz8jy"\n')
    temp.write('\t\tset comment ''\n')                            
    temp.write('\t\tset one-arm-ips-urlfilter disable\n')
    temp.write('\t\tset ip-addr-block disable\n')
    temp.write('\t\tconfig entries\n')
    for reg in arqEnt:
        temp.write('\t\t\tedit %i\n' %(S+1))
        temp.write('\t\t\t\tset url "%s"\n' %arqEnt[reg])
        temp.write('\t\t\t\tset type wildcard\n')
        temp.write('\t\t\t\tset action allow\n')
        temp.write('\t\t\t\tset status enable\n')
        temp.write('\t\t\t\tset web-proxy-profile \'\'\n')
        temp.write('\t\t\t\tset referrer-host \'\'\n')
        temp.write('\t\t\tnext\n')
        S += 1
    temp.write('\t\tend\n')
    temp.write('\tnext\n')
    temp.write('end')            
    temp.close()
    return urlArq, S
def main():
    print(70*'-')
    print("Phyton: ", os.path.realpath(__file__))
    geraCmd = True
    while geraCmd:
        print(70*'-')
        urlArq = input('Informe nome do arquivo de URLs(.txt) ou "PARE": ')
        if "PARE" in urlArq.upper():
            geraCmd = False
            sys.exit()
        P = os.path.dirname(os.path.realpath(__file__))
        urlArq = tryTxt(P, urlArq)
        arqEnt, E = lerTxt(P, urlArq)
        print('\n\t\t\t%4i URLs lidas em %s.txt' %(E, urlArq))
        urlArq, S = gravaTxt(P, urlArq.upper(), E, arqEnt)
        print('\t\t\t%4i Comandos criados em %s \n' %(S, urlArq+"-cmd.txt"))
main()
