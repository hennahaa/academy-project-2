# AW ACADEMY RYHMÄTYÖ 2
## Konttiprojekti

[Anna1hanen](https://github.com/Anna1hanen) | hennahaa | [KirsiHolmberg](https://github.com/KirsiHolmberg)

Pohjana käytetty koodi: https://github.com/runeli/assesment-test

Pohja käyttää flaskia https://flask.palletsprojects.com/en/2.0.x/

Muokattu käyttämään PosgreSQL:ää.

## Ohje

Luo ensin GCP Artifact Registryyn Docker-repo

    gcloud artifacts repositories create REPOSITORY \
        --project=PROJECT\
        --repository-format=docker \
        --location=LOCATION \
        --description="Docker repository"

Buildaa image

    docker build . -t <haluamasi-imagen nimi>  

Tägää luomasi image

    docker tag <haluamasi-imagen-nimi> LOCATION-docker.pkg.dev/PROJECT/REPOSITORY/<haluamasi-imagen-nimi-repossa>

Pushaa tämä

    docker push LOCATION.pkg.dev/PROJECT/REPOSITORY/<haluamasi-imagen-nimi-repossa>

Luo K8S cluster (zone samalla alueella kuin location)  

    gcloud container clusters create CLUSTER \
    --num-nodes 1 \
    --zone COMPUTE_ZONE

Deployaa .yamlit  
    
    kubectl apply -f <tiedostonnimi>.yaml

Muista korjata `secrets.yaml` configmapiin Postgresin Nodeportin Internal IP-osoite

Tässä kohtaa voi myös asettaa pätevän salasanan `secrets.yaml`-tiedoston `POSTGRES_PASSWORD`-muuttujaan. Muuttujan luoda linuxissa seuraavasti:

    echo "HALUAMASI_SALASANA" | base64

Ja tämä palauttaa salasanan secretsin haluamassa muodossa.

`blog_app.yaml` deploymentin `image:`-kohtaan on täydennettävä luomasi container-imagen osoite artifact registeryssa. Eli jotain seuraavaa: `LOCATION.pkg.dev/PROJECT/REPOSITORY/<haluamasi-imagen-nimi-repossa>`

Lopuksi vielä luo tietokanta (`schema.sql`) postgres-servicen loadbalancerin External IP:n kautta.

    psql -h EXTERNAL-IP -p 5432 -d postgresdb -U postgresadmin -W

(Postgresin loadbalancerin voi halutessaan poistaa tämän jälkeen. Se sijaitsee tiedostossa `postgres.yaml`)

---

Ohje *ei* ota kantaa onko komentoihin tarvittava autentikaatio kunnossa. Allaolevista linkeistä on apua näissä ongelmissa:

[Setting up authentication for Docker](https://cloud.google.com/artifact-registry/docs/docker/authentication)

[Troubleshooting Cloud Endpoints in GKE](https://cloud.google.com/endpoints/docs/openapi/troubleshoot-gke-deployment)



