from datetime import datetime, timedelta
from app.database import SessionLocal
from app import models


def seed_news():
    db = SessionLocal()
    try:
        if db.query(models.News).first():
            return

        sample_news = [
            {
                "title": "FastAPI se consolida como framework líder para APIs em Python",
                "content": "O FastAPI continua ganhando espaço no ecossistema Python graças à sua alta performance, validação automática via Pydantic e documentação interativa gerada em tempo real. Empresas de todos os tamanhos adotam a ferramenta para construir microsserviços robustos e escaláveis.",
                "image_url": "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/gri3werw3xim/b/bucket-imagens/o/img-tech-1.jpg",
                "published_at": datetime.utcnow() - timedelta(days=1),
            },
            {
                "title": "Automação de tarefas repetitivas com Python e n8n",
                "content": "Combinar Python com plataformas de automação como o n8n permite criar fluxos inteligentes que integram planilhas, e-mails, bancos de dados e APIs. O resultado é a redução de erros manuais e ganho expressivo de produtividade nas operações diárias.",
                "image_url": None,
                "published_at": datetime.utcnow() - timedelta(days=3),
            },
            {
                "title": "Oracle Cloud Free Tier: hospede suas aplicações sem custo",
                "content": "A Oracle Cloud oferece instâncias sempre gratuitas ideais para projetos pessoais, portfólios e pequenas APIs. Com VMs ARM e x86 disponíveis, desenvolvedores podem manter aplicações em produção sem pagar nada durante o ciclo de vida do projeto.",
                "image_url": "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/gri3werw3xim/b/bucket-imagens/o/img-tech-2.jpg",
                "published_at": datetime.utcnow() - timedelta(days=7),
            },
            {
                "title": "Inteligência Artificial generativa no dia a dia do desenvolvedor",
                "content": "Assistentes de IA estão transformando a forma como escrevemos código, documentamos sistemas e resolvemos bugs. Aprender a usar essas ferramentas de forma crítica e ética tornou-se uma habilidade essencial para profissionais de tecnologia.",
                "image_url": None,
                "published_at": datetime.utcnow() - timedelta(days=10),
            },
            {
                "title": "Docker para iniciantes: containerizando aplicações Python",
                "content": "Docker simplifica o deploy de aplicações Python ao empacotar código, dependências e configurações em containers isolados. Com um Dockerfile bem escrito, é possível garantir que sua aplicação rode da mesma forma em desenvolvimento e produção.",
                "image_url": "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/gri3werw3xim/b/bucket-imagens/o/img-docker-1.jpg",
                "published_at": datetime.utcnow() - timedelta(days=14),
            },
            {
                "title": "Boas práticas de segurança em APIs REST",
                "content": "Autenticação, autorização, validação de entrada, rate limiting e logs adequados são pilares fundamentais para proteger APIs REST. Ignorar essas práticas pode expor dados sensíveis e comprometer toda a infraestrutura de uma aplicação.",
                "image_url": None,
                "published_at": datetime.utcnow() - timedelta(days=21),
            },
            {
                "title": "SQLAlchemy 2.0: novidades e padrões modernos",
                "content": "A versão 2.0 do SQLAlchemy trouxe uma API mais consistente, suporte aprimorado a tipos e novas formas de consulta. Adotar esses padrões modernos melhora a legibilidade do código e facilita a manutenção de projetos de longo prazo.",
                "image_url": "https://objectstorage.sa-saopaulo-1.oraclecloud.com/n/gri3werw3xim/b/bucket-imagens/o/img-sqlalchemy-1.jpg",
                "published_at": datetime.utcnow() - timedelta(days=30),
            },
        ]

        for item in sample_news:
            db.add(models.News(**item))

        db.commit()
    finally:
        db.close()
