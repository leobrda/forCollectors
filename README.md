# 🛡️ ForCollectors - v1.0.0

O **EduDash** é uma plataforma full-stack robusta desenvolvida para colecionadores organizarem seus acervos. O sistema oferece uma experiência completa de gerenciamento, desde o cadastro seguro até a manipulação de mídia na nuvem.

## 🚀 Tecnologias e Dependências

O projeto utiliza uma stack moderna focada em escalabilidade e facilidade de manutenção:

*   **Framework Web:** Django 6.0.4.
*   **Interface:** Tailwind CSS e Alpine.js para uma UI responsiva e interativa.
*   **Gestão de Imagens:** Cloudinary (armazenamento) integrado via `django-cloudinary-storage`.
*   **Otimização de Storage:** `django-cleanup` para remoção automática de arquivos órfãos no Cloudinary ao deletar itens.
*   **Segurança:** `python-decouple` para gestão de variáveis de ambiente e segredos.
*   **Infraestrutura:** Totalmente conteinerizado com Docker e Docker Compose.
*   **Servidor de Produção:** Gunicorn pronto para deploy.

## ✨ Funcionalidades Implementadas

- [x] **Autenticação Avançada:** Cadastro com e-mail obrigatório e login seguro.
- [x] **Recuperação de Conta:** Fluxo completo de redefinição de senha via link enviado por e-mail (SMTP).
- [x] **Gestão de Coleções (CRUD):** Organização de itens em álbuns com descrições detalhadas.
- [x] **Tratamento de Mídia:** Upload automático para a nuvem e visualização em galeria.
- [x] **Layout Blindado:** Interface responsiva com tratamento contra quebra de layout por textos longos (Truncate/Break-words).

## 🛠️ Como rodar o projeto

### Via Docker (Recomendado)
```bash
# 1. Clone o repositório
git clone [https://github.com/leobrda/forCollectors.git](https://github.com/leobrda/forCollectors.git)

# 2. Configure o arquivo .env com suas chaves (Cloudinary, SMTP, etc)

# 3. Suba os containers
docker-compose up --build
