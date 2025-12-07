# Meme Generator
Enostavna Flask aplikacija za ustvarjanje memov (upload slike + zgornji in spodnji text)

## Zahteve
- Docker
- (opcijsko) docker-compose

## Zagon
1. Build:
   ```bash
   docker build -t meme-generator
2. Run:
   ```bash
   docker run -p 5000:5000 meme-generator
3. Uporaba:
   Obiščite http://localhost:5000 in naložite sliko ter vnesite zgornji in spodnji text.
   Rezultat je generiran meme.  
