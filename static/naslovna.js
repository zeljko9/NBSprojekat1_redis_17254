export class Naslovna{
    constructor(){
        this.kontejner=null;
    }    

    crtajNaslovnu(host){
        this.kontejner=document.createElement("div");
        this.kontejner.className="naslovna";
        host.appendChild(this.kontejner);
        
        let labela=document.createElement("label");
        labela.innerHTML="Vase ime:"
        this.kontejner.appendChild(labela)

        let tb1= document.createElement("input");
        tb1.className="ime";
        this.kontejner.appendChild(tb1);

        labela=document.createElement("label");
        labela.innerHTML="Vas mejl:"
        this.kontejner.appendChild(labela)

        let tb2= document.createElement("input");
        tb2.className="mejl";
        this.kontejner.appendChild(tb2);

        labela=document.createElement("label");
        labela.innerHTML="Zanrovi:"
        this.kontejner.appendChild(labela)

        let tb3= document.createElement("input");
        tb3.className="Zanrovi";
        this.kontejner.appendChild(tb3);

        const dugme = document.createElement("button");
        dugme.innerHTML="Pretplati se";
        this.kontejner.appendChild(dugme);
        dugme.onclick=(ev)=>{
            if(tb1.value=="")
                return;
            if(tb2.value=="")
                return;
            if(tb3.value=="")
                return;

            const regex1=/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
            if(!tb2.value.match(regex1)){
                alert("Unesite validan mejl.");
            }

            const regex2=/[a-zA-Z]+,[a-zA-Z]/g
            if(!tb3.value.match(regex2)){
                alert("Format zanrova je: zanr1,zanr2,zanr3");
            }

            fetch("http://localhost:5000/PretplatiSe", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                body: JSON.stringify({
                    ime:tb1.value,
                    mejl: tb2.value,
                    zanrovi: tb3.value
                })
            })
            .then(response=>response.json())
            .then(data => {
                if(data=="dodato"){
                    alert("Uspesno ste pretplaceni!")
                }
                else if(data=="azurirano"){
                    alert("Uspesno ste azurirali zanrove na vec postojeci nalog!")
                }
            }).catch(p => {
                tb1.value="";
                tb2.value="";
                tb3.value="";
                alert("Greška prilikom upisa.");
            });
        }

        document.write("<br>");
        document.write("<br>");

        let Dlabela=document.createElement("label");
        Dlabela.innerHTML="Vas mejl prethodno pretplacen:"
        let Dmejl=document.createElement("input");
        Dmejl.className="Dmejl";
        let Ddugme=document.createElement("button");
        Ddugme.innerHTML="Prekini pretplatu";
        Ddugme.onclick=(ev)=>{
            if(Dmejl.value==""){
                alert("Molimo Vas unesite mejl adresu");
            }
            const regex1=/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/g;
            if(!Dmejl.value.match(regex1)){
                alert("Unesite validan mejl.");
            }

            fetch("http://localhost:5000/DePretplata", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                body: JSON.stringify({
                    mejl:Dmejl.value
                })
            }).then(p => {
                if (p.ok) {
                    Dmejl.value="";
                    alert("Uspesna de-pretplata!");
                }
            }).catch(p => {
                alert("Proverite mejl adresu jos jednom, da li ste sigurni da ste vec pretplaceni?");
            });

        }

        this.kontejner.appendChild(Dlabela);
        this.kontejner.appendChild(Dmejl);
        this.kontejner.appendChild(Ddugme);



    }
}