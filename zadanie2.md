# Sprawozdanie z Laboratorium: Zadanie 2

## 1. Konfiguracja etapów łańcucha (Pipeline)
W ramach zadania opracowano automatyczny łańcuch GitHub Actions, który realizuje następujące kroki:
- **Bezpieczeństwo poświadczeń:** Logowanie do Docker Hub w celu obsługi pamięci podręcznej (cache) zrealizowano przy użyciu bezpiecznych zmiennych `GitHub Secrets` (`DOCKERHUB_USERNAME` oraz `DOCKERHUB_TOKEN`).
- **Wsparcie dla architektur:** Wykorzystano emulację QEMU oraz Docker Buildx, co pozwala na jednoczesne budowanie obrazu dla architektur `linux/amd64` oraz `linux/arm64`.
- **Obsługa Cache:** Konfiguracja cache wykorzystuje zewnętrzny rejestr na Docker Hub w trybie `mode=max` (zarówno pobieranie `cache-from`, jak i wysyłanie `cache-to`), co optymalizuje czas budowania kolejnych warstw obrazu.

## 2. Test CVE i mechanizm blokady (Weryfikacja działania)
Do realizacji testów bezpieczeństwa wybrano skaner **Trivy**. Został on skonfigurowany w trybie restrykcyjnym (`exit-code: '1'`) dla zagrożeń o statusie `HIGH` oraz `CRITICAL`.

Zgodnie z wymaganiami projektowymi, proces budowania celowo zatrzymuje się na tym etapie:
- Skaner Trivy wykrył w obrazie bazowym podatności sklasyfikowane jako wysokie/krytyczne.
- Pipeline zwrócił kod błędu (Exit Code 1), co **skutecznie zablokowało** wykonanie kolejnego kroku (wypchnięcia obrazu do rejestru GHCR).
- Cel projektowy został osiągnięty: system dystrybucji kodu zabezpiecza publiczne repozytorium przed publikacją obrazu zawierającego krytyczne zagrożenia.
- Załączony został zrzut ekranu (Github_actions.png) pokazujący wyniki z Github Actions

## 3. Strategia tagowania (Uzasadnienie - dodatkowe punkty)
W projekcie przyjęto następujący schemat tagowania, oparty o dobre praktyki (best practices) automatyzacji:
- **Dla obrazów docelowych (GHCR):** Stosowany jest podwójny tag: `latest` (wskazuje na najnowszą stabilną wersję) oraz unikalny skrócony hash commita z Gita (`sha-XXXXX`). Użycie SHA zapewnia **niezmienność obrazu** (*immutability*). Pozwala to na dokładne odtworzenie stanu aplikacji z konkretnego momentu w historii kodu i zapobiega przypadkowemu nadpisaniu działającej wersji na produkcji.
- **Dla danych Cache (Docker Hub):** Cache tagowany jest nazwą gałęzi (np. `cache-main`). Dzięki temu kolejne commity w obrębie tej samej gałęzi współdzielą warstwy, drastycznie przyspieszając pracę deweloperską, bez jednoczesnego mieszania pamięci podręcznej pomiędzy różnymi funkcjonalnościami (branchami) aplikacji.
