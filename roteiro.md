## **Compartilhamento de Arquivos P2P**

*Naspter* com *RMI*

**Docente:** Lo Silva Sampaio |
**RA:** 11201812025 | **NA1**
___

### **Roteiro:**

     01. Aplicação: 
         Python | Bibliotecas

     02. Ambiente: 
         Peers | Código | Terminal

     03. Inicialização servidor:
         * obrigatoriamente inicializado primeiro;

     04. Inicialização peer 1;

     05. Join peer 1:
         Request: "join" | peer 1
         Response: "ok"  | servidor 

     06. Inicialização peer 2;

     07. Join peer 2:
         Request: "join" | peer 2
         Response: "ok"  | servidor 

     08. Inicialização peer 3;

     09. Join peer 3:
         Request: "join" | peer 3
         Response: "ok"  | servidor 

     10. Search peer 3:
         Request: "arquivos de peers"  | peer 3
         Response: "lista de arquivos" | servidor
         ________________________________________
         Esperado: 
         "rupaul.mp4"    | peer 1 
         "sucession.mp4" | peer 2
         "null"          | peer 3

     11. Donwload do arquivo (2 Gb):
         Request: "rupaul.mp4"         | peer 3
         Response: "accept or reject"  | peer 1

     12. Mostrar execução do arquivo;

     13. Search peer 2 (verificar update):
         Request: "arquivos de peers"  | peer 2
         Response: "lista de arquivos" | servidor
         ________________________________________
         Esperado: "rupaul.mp4" | peer 1 + peer 3
    
    14. Concluir.