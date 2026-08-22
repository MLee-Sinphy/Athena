# Validação da versão 1.0.0

## Evidências automatizadas

- TEST-071: regressão de autenticação, autorização, rate limit, uploads, CORS, cabeçalhos seguros e configuração de produção.
- TEST-072: scripts de backup/restauração cifram banco e mídia, verificam SHA-256 e exigem confirmação destrutiva.
- TEST-073: catálogo paginado limita respostas a 100 itens e `scripts/load_test.py` permite simular 500 clientes concorrentes.
- TEST-074: Playwright executa as jornadas responsivas e Axe em Chromium, Firefox e WebKit.

## Procedimento de carga

No ambiente de homologação com dados sintéticos representativos, execute:

```bash
python backend/manage.py seed_load_data --readers 5000 --titles 20000 --copies 50000
python3 scripts/load_test.py https://DOMINIO/api/v1/health/ --clients 500
```

Registre hardware, versão/imagem, duração, sucessos, falhas, mediana e p95. O script mede uma rajada concorrente de disponibilidade, não substitui perfil prolongado de tráfego nem teste do catálogo autenticado.

## Itens de aceite externo

- TEST-070: publicar GitHub Pages e VPS reais; verificar HTTPS, CORS e mensagem do frontend com backend desligado.
- TEST-072: restaurar uma cópia real em ambiente isolado e comparar banco/mídia.
- TEST-073: executar a simulação no VPS alvo e registrar o resultado medido.
- TEST-074: revisar duas versões estáveis disponíveis e validar NVDA/Firefox, VoiceOver/Safari e ampliação de 200–400%.
- Aceite funcional final pelo responsável.

Nenhum item acima deve ser marcado como aprovado por inferência. A tag `1.0.0`, o changelog de entrega e o merge em `main` só ocorrem depois desse aceite.
