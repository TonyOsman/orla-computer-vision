# Modelo de landmarks

O ZIP local inclui `shape_predictor_68_face_landmarks.dat` para execução sem download na apresentação. O arquivo não deve ser incluído no commit Git; consta no `.gitignore`.

Fonte usada pelo professor: https://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

No repositório publicado, baixar e descompactar esse arquivo na pasta `modelos`, mantendo o nome original. No Linux, os comandos `wget` e `bzip2 -d` aparecem no laboratório de dlib. No Windows pode-se descompactar com ferramenta de arquivos instalada.

SHA-256 do `.dat` utilizado: `fbdc2cb80eb9aa7a758672cbfdda32ba6300efe9b6e6c7a299ff7e736b11b92f`.

É um modelo pré-treinado de landmarks; os alunos não o treinaram. O exemplo oficial do dlib informa restrição de uso comercial relacionada ao dataset iBUG 300-W. Este trabalho é um protótipo acadêmico, não uma autorização de uso comercial pela Orla.

Referência: https://dlib.net/face_landmark_detection.py.html
