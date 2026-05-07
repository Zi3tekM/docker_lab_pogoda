# docker_lab_pogoda
Sprawozdanie: Zadanie 1 - Programowanie Aplikacji w Chmurze Obliczeniowej   

Autor: Michał Ziętek

# 1. Kod źródłowy aplikacji
  Aplikacja została opracowana w języku Python przy użyciu frameworka Flask.  
  
  Funkcjonalność:  
  Logi startowe (Wymóg 1a): Po uruchomieniu kontenera aplikacja pozostawia w logach informację o dacie uruchomienia, autorze oraz porcie TCP.  
  Interfejs użytkownika (Wymóg 1b): Aplikacja pozwala na wybór kraju (Polska, Niemcy, Francja) oraz miasta z listy.  
  Dane pogodowe: System wyświetla aktualną temperaturę, wilgotność, prędkość wiatru, ciśnienie, opady oraz zachmurzenie w wybranej lokalizacji wraz z czasem pomiaru.

# 2. Plik Dockerfile
  Zastosowano:  
  Wieloetapowe budowanie obrazu (multi-stage build).  
  Obraz bazowy Alpine Linux dla minimalizacji rozmiaru.  
  Instrukcję HEALTHCHECK dla monitorowania stanu aplikacji.  
  Metadane autora zgodne ze standardem OCI.

# 3. Polecenia Docker

  Zbudowanie opracowanego obrazu kontenera:  
  docker build -t cloud-app-lab1:latest .

  Uruchomienie kontenera na podstawie zbudowanego obrazu:  
  docker run -d -p 5000:5000 --name moj-kontener-pogoda cloud-app-lab1:latest

  Uzyskanie informacji z logów aplikacji:  
  docker logs moj-kontener-pogoda

  Polecenie do sprawdzenia warstw:  
  docker history nazwa_obrazu

  Polecenie do sprawdzenia rozmiaru:  
  docker images cloud-app-lab1:latest
