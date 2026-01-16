"""
Présentation du Projet MLOps - Détection de Fraude
Version statique 100% explicative (aucun code affiché)
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Détection de Fraude - Présentation MLOps",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé pour un design professionnel
st.markdown("""
<style>
    /* Couleurs et thème */
    :root {
        --primary-color: #dc3545;
        --secondary-color: #0066cc;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --dark-bg: #1e1e1e;
        --light-bg: #f8f9fa;
    }
    
    /* Titres personnalisés */
    .main-title {
        text-align: center;
        color: #dc3545;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 20px 0;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.4rem;
        color: #555;
        margin-top: 8px;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    /* Cards et boîtes */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        color: white;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    }
    
    .info-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #0066cc;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        color: #1a1a1a;
    }
    
    .info-box p, .info-box ul, .info-box li {
        color: #1a1a1a;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #28a745;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        color: #1a1a1a;
    }
    
    .success-box p, .success-box ul, .success-box li {
        color: #1a1a1a;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ffc107;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        color: #1a1a1a;
    }
    
    .warning-box p, .warning-box ul, .warning-box li {
        color: #1a1a1a;
    }
    
    .danger-box {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #dc3545;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        color: #1a1a1a;
    }
    
    .danger-box p, .danger-box ul, .danger-box li {
        color: #1a1a1a;
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
        border-top: 4px solid #dc3545;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #dc3545;
        margin: 10px 0;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        margin: 20px 0;
        font-size: 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Liste avec puces personnalisées */
    .custom-list {
        font-size: 1.1rem;
        line-height: 2;
        color: #1a1a1a;
    }
    
    .custom-list li {
        margin: 10px 0;
        padding-left: 10px;
        color: #1a1a1a;
    }
    
    /* Timeline */
    .timeline-item {
        border-left: 3px solid #dc3545;
        padding-left: 20px;
        margin: 20px 0;
        position: relative;
    }
    
    .timeline-item::before {
        content: '●';
        position: absolute;
        left: -8px;
        color: #dc3545;
        font-size: 1.5rem;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        margin: 5px;
        font-size: 0.9rem;
    }
    
    .badge-primary {
        background: #0066cc;
        color: white;
    }
    
    .badge-success {
        background: #28a745;
        color: white;
    }
    
    .badge-warning {
        background: #ffc107;
        color: #333;
    }
    
    .badge-danger {
        background: #dc3545;
        color: white;
    }
    
    /* Divider */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #dc3545, transparent);
        margin: 30px 0;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .feature-item {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .feature-item h4 {
        color: #667eea;
        margin-bottom: 10px;
    }
    
    /* Highlight text */
    .highlight {
        background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Navigation avec style amélioré
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; margin-bottom: 20px; color: white;'>
        <h1 style='margin:0; font-size: 2rem;'>🚨</h1>
        <h2 style='margin:10px 0 0 0; font-size: 1.3rem;'>MLOps Fraude</h2>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "📑 Navigation",
    [
        "🏠 Vue d'ensemble",
        "🧹 Nettoyage des données",
        "⚙️ Ingénierie des features",
        "🤖 Modèle Autoencoder",
        "🎯 API de prédiction",
        "🐳 Docker & MLOps",
        "📊 Tableau de bord",
        "📧 Alertes email",
        "📈 Résultats & KPIs",
        "🔍 Architecture technique",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; color: white;'>
        <p style='margin: 0; font-size: 0.9rem;'><strong>📊 Projet MLOps</strong></p>
        <p style='margin: 5px 0 0 0; font-size: 0.8rem;'>Détection de fraude temps réel</p>
        <p style='margin: 5px 0 0 0; font-size: 0.8rem;'>🎓 Production Ready</p>
    </div>
""", unsafe_allow_html=True)


def titre(t, stitre="", icon="🚨"):
    st.markdown(
        f"""
        <div class='fade-in'>
            <h1 class='main-title'>{icon} {t}</h1>
            {f"<p class='sub-title'>{stitre}</p>" if stitre else ""}
            <div class='divider'></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, icon="📊"):
    return f"""
    <div class='metric-card'>
        <div style='font-size: 2.5rem; margin-bottom: 10px;'>{icon}</div>
        <div style='font-size: 2rem; font-weight: 700; margin: 10px 0;'>{value}</div>
        <div style='font-size: 1rem; opacity: 0.9;'>{label}</div>
    </div>
    """


def info_box(content, box_type="info"):
    return f"<div class='{box_type}-box'>{content}</div>"


def success_box(content):
    return f"<div class='success-box'>{content}</div>"


def warning_box(content):
    return f"<div class='warning-box'>{content}</div>"


def danger_box(content):
    return f"<div class='danger-box'>{content}</div>"


if page == "🏠 Vue d'ensemble":
    titre("Détection de Fraude MLOps", "Pipeline complet de production : données → modèle → déploiement → monitoring → alertes", "🏠")

    # Hero section avec métriques clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(metric_card("Accuracy", "93.5%", "🎯"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(metric_card("Rappel Fraude", "87.1%", "🔍"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(metric_card("ROC-AUC", "98.2%", "📈"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(metric_card("API Response", "~137ms", "⚡"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Objectif du projet
    st.markdown("<div class='section-header'>🎯 Objectif du Projet</div>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <h3 style='margin-top:0; color: #0066cc;'>Système de détection de fraude production-ready</h3>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
        Concevoir et déployer une solution MLOps complète capable de détecter les transactions frauduleuses 
        en temps réel avec une architecture évolutive, un monitoring avancé et des alertes automatiques. 
        Le système traite les transactions instantanément, génère des prédictions fiables et notifie 
        les équipes métiers dès qu'une anomalie est détectée.
        </p>
        <p style='font-size: 1.05rem; margin-top: 15px;'>
        <strong>🎓 Contexte :</strong> Projet académique démontrant les compétences en Machine Learning, 
        DevOps, déploiement cloud-ready et monitoring opérationnel.
        </p>
    """), unsafe_allow_html=True)

    # Points forts
    st.markdown("<div class='section-header'>✨ Points Forts du Système</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🔄 Pipeline Complet</h4>
            <ul class='custom-list'>
                <li><strong>Ingestion :</strong> Nettoyage PaySim 6M+ transactions</li>
                <li><strong>Features :</strong> 27 variables production-ready</li>
                <li><strong>Modèle :</strong> Autoencoder optimisé (9,579 params)</li>
                <li><strong>API :</strong> FastAPI temps réel (&lt;200ms)</li>
                <li><strong>Monitoring :</strong> Dashboard 5 pages Streamlit</li>
                <li><strong>Alertes :</strong> Notifications SMTP instantanées</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🚀 Prêt Production</h4>
            <ul class='custom-list'>
                <li><strong>Sans historique :</strong> Features calculables sur transaction unique</li>
                <li><strong>Conteneurisé :</strong> Docker Compose multi-services</li>
                <li><strong>Scalable :</strong> Architecture microservices</li>
                <li><strong>Observabilité :</strong> Logs JSONL + métriques temps réel</li>
                <li><strong>Sécurisé :</strong> Variables d'env + healthchecks</li>
                <li><strong>Documenté :</strong> README MLOps complet</li>
            </ul>
        """), unsafe_allow_html=True)

    # Pipeline visuel
    st.markdown("<div class='section-header'>🔗 Architecture du Pipeline</div>", unsafe_allow_html=True)
    
    pipeline_steps = [
        ("1️⃣ Nettoyage", "PaySim 6.3M → 49K transactions équilibrées", "#667eea"),
        ("2️⃣ Feature Engineering", "9 entrées brutes → 27 features avancées", "#764ba2"),
        ("3️⃣ Entraînement", "Autoencoder sur transactions normales uniquement", "#f093fb"),
        ("4️⃣ API FastAPI", "POST /predict + transformation + scoring", "#4facfe"),
        ("5️⃣ Monitoring", "Dashboard 5 pages (temps réel, analytics, perf)", "#00f2fe"),
        ("6️⃣ Alertes", "Email SMTP si fraude détectée", "#43e97b"),
        ("7️⃣ Docker", "Orchestration API + Dashboard + volumes", "#38f9d7"),
    ]
    
    for step, desc, color in pipeline_steps:
        st.markdown(f"""
            <div class='timeline-item' style='border-left-color: {color};'>
                <h4 style='color: {color}; margin: 0;'>{step}</h4>
                <p style='margin: 5px 0 0 0; font-size: 1.05rem;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    # Technologies
    st.markdown("<div class='section-header'>🛠️ Stack Technologique</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🐍</div>
                <h4 style='color: #667eea;'>Core ML</h4>
                <p style='line-height: 1.8;'>
                    <span class='badge badge-primary'>Python 3.11</span><br>
                    <span class='badge badge-primary'>TensorFlow/Keras</span><br>
                    <span class='badge badge-primary'>Pandas/NumPy</span><br>
                    <span class='badge badge-primary'>Scikit-learn</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🌐</div>
                <h4 style='color: #667eea;'>API & Dashboard</h4>
                <p style='line-height: 1.8;'>
                    <span class='badge badge-success'>FastAPI</span><br>
                    <span class='badge badge-success'>Streamlit</span><br>
                    <span class='badge badge-success'>Uvicorn</span><br>
                    <span class='badge badge-success'>SMTP (smtplib)</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🐳</div>
                <h4 style='color: #667eea;'>DevOps & Infra</h4>
                <p style='line-height: 1.8;'>
                    <span class='badge badge-warning'>Docker</span><br>
                    <span class='badge badge-warning'>Docker Compose</span><br>
                    <span class='badge badge-warning'>Volumes</span><br>
                    <span class='badge badge-warning'>Health Checks</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Chiffres clés du projet
    st.markdown("<div class='section-header'>📊 Chiffres Clés du Projet</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics = [
        ("49,977", "Transactions", "📝"),
        ("27", "Features", "⚙️"),
        ("9,579", "Paramètres", "🧠"),
        ("~137ms", "Latence API", "⚡"),
        ("5", "Pages Dashboard", "📊"),
    ]
    
    for col, (value, label, icon) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
                <div style='text-align: center; padding: 15px; background: white; border-radius: 10px; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.08); border-top: 3px solid #dc3545;'>
                    <div style='font-size: 2rem;'>{icon}</div>
                    <div class='stat-number' style='font-size: 1.8rem;'>{value}</div>
                    <div class='stat-label' style='font-size: 0.85rem;'>{label}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to action
    st.markdown(warning_box("""
        <h4 style='margin-top: 0; color: #ff6b6b;'>🚀 Prochaines Étapes Recommandées</h4>
        <p style='font-size: 1.05rem; line-height: 1.8;'>
        <strong>Pour explorer :</strong> Naviguez dans les sections via le menu latéral pour comprendre chaque 
        composant du pipeline (données, features, modèle, API, déploiement).<br>
        <strong>Pour tester :</strong> Lancez <code>docker-compose up</code> pour démarrer API (port 8000) 
        et Dashboard (port 8501).<br>
        <strong>Pour adapter :</strong> Consultez les fichiers README pour personnaliser SMTP, 
        seuil de détection ou features.
        </p>
    """), unsafe_allow_html=True)


elif page == "🧹 Nettoyage des données":
    titre("Nettoyage des Données", "Source : Dataset PaySim (simulation mobile money)", "🧹")

    # Stats avant/après
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class='stat-card' style='border-top-color: #dc3545;'>
            <h3 style='color: #dc3545; margin: 0;'>📥 Dataset Original</h3>
            <div class='stat-number'>6.36M</div>
            <div class='stat-label'>Transactions sur 30 jours</div>
            <hr style='margin: 15px 0;'>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Taux fraude :</strong> 0.13%</p>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Fraudes :</strong> 8,213</p>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Source :</strong> PaySim simulator</p>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""<div class='stat-card' style='border-top-color: #28a745;'>
            <h3 style='color: #28a745; margin: 0;'>📤 Dataset Final</h3>
            <div class='stat-number'>49,977</div>
            <div class='stat-label'>Transactions échantillonnées</div>
            <hr style='margin: 15px 0;'>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Taux fraude :</strong> 16.43%</p>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Fraudes :</strong> 8,213 (conservées)</p>
            <p style='font-size: 1.1rem; margin: 5px 0; color: #1a1a1a;'><strong>Fichier :</strong> paysim_reduced.csv</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Description du dataset
    st.markdown("<div class='section-header'>📋 Description du Dataset PaySim</div>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <p style='font-size: 1.1rem; line-height: 1.8;'>
        <strong>PaySim</strong> est un simulateur de transactions de paiement mobile basé sur un mois réel 
        d'activité d'un service africain. Il génère des transactions synthétiques réalistes incluant :
        </p>
        <ul class='custom-list'>
            <li><strong>Types de transactions :</strong> PAYMENT, TRANSFER, CASH_OUT, CASH_IN, DEBIT</li>
            <li><strong>Métadonnées temporelles :</strong> Step (heure du mois), montant, soldes avant/après</li>
            <li><strong>Comptes :</strong> Origine (toujours client C*), Destination (client ou marchand M*)</li>
            <li><strong>Label fraude :</strong> isFraud (binaire), isFlaggedFraud (montants suspects >200K)</li>
        </ul>
        <p style='font-size: 1.05rem; margin-top: 10px; color: #666;'>
        <strong>📊 Challenge :</strong> Déséquilibre de classe massif (0.13%) nécessitant rééquilibrage pour entraîner un modèle efficace.
        </p>
    """), unsafe_allow_html=True)

    # Pipeline de nettoyage
    st.markdown("<div class='section-header'>🔧 Étapes de Nettoyage</div>", unsafe_allow_html=True)
    
    steps = [
        ("1. Vérification Valeurs Manquantes", "Analyse complète : <strong>0 valeur manquante</strong> détectée. Dataset propre.", "success"),
        ("2. Suppression Doublons", "Identification et retrait des lignes dupliquées (si existantes).", "info"),
        ("3. Validation Types", "Vérification types de colonnes : numériques (amount, balances, step) et catégorielles (type).", "info"),
        ("4. Contrôle Cohérence", "<strong>Montants négatifs :</strong> 0 trouvés<br><strong>Incohérences solde :</strong> Vérifiées (origine/destination).", "success"),
        ("5. Échantillonnage Stratifié", "Réduction 6.36M → 49,977 lignes en <strong>conservant toutes les fraudes</strong> + échantillon transactions normales.<br><strong>Ratio final fraude :</strong> 16.43% (exploitable pour ML).", "warning"),
        ("6. Export Dataset", "Sauvegarde finale : <code>paysim_reduced.csv</code> (prêt pour feature engineering).", "success"),
    ]
    
    for title, desc, box_type in steps:
        st.markdown(f"""
            <div class='{box_type}-box' style='margin: 15px 0;'>
                <h4 style='margin-top: 0;'>{title}</h4>
                <p style='font-size: 1.05rem; line-height: 1.7; margin: 0;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    # Colonnes conservées
    st.markdown("<div class='section-header'>📊 Colonnes du Dataset Final</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>⏱️ Temporelles</h4>
            <ul>
                <li><strong>step</strong> : Heure (0-743)</li>
            </ul>
            <h4 style='color: #667eea; margin-top: 15px;'>🏷️ Catégorielles</h4>
            <ul>
                <li><strong>type</strong> : Type transaction</li>
                <li><strong>nameOrig</strong> : Compte origine</li>
                <li><strong>nameDest</strong> : Compte destination</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>💰 Montants</h4>
            <ul>
                <li><strong>amount</strong> : Montant transaction</li>
                <li><strong>oldbalanceOrg</strong> : Solde avant (origine)</li>
                <li><strong>newbalanceOrig</strong> : Solde après (origine)</li>
                <li><strong>oldbalanceDest</strong> : Solde avant (dest)</li>
                <li><strong>newbalanceDest</strong> : Solde après (dest)</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col3:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🎯 Labels</h4>
            <ul>
                <li><strong>isFraud</strong> : Label fraude (0/1)</li>
                <li><strong>isFlaggedFraud</strong> : Flagged suspicious</li>
            </ul>
            <h4 style='color: #28a745; margin-top: 15px;'>✅ Qualité</h4>
            <p><strong>Valeurs manquantes :</strong> 0</p>
            <p><strong>Doublons :</strong> Supprimés</p>
            <p><strong>Types :</strong> Validés</p>
        """), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(warning_box("""
        <h4 style='margin-top: 0;'>⚠️ Décision Stratégique : Échantillonnage</h4>
        <p style='font-size: 1.05rem; line-height: 1.7;'>
        L'échantillonnage stratifié permet de :<br>
        ✅ <strong>Garder toutes les fraudes</strong> (8,213) pour maximiser l'apprentissage<br>
        ✅ <strong>Réduire les normales</strong> (41,764 sur 6.35M) pour équilibrer le dataset<br>
        ✅ <strong>Accélérer l'entraînement</strong> tout en maintenant la représentativité<br>
        ✅ <strong>Ratio 16.43%</strong> : suffisant pour entraîner un Autoencoder (modèle sur normales uniquement)
        </p>
    """), unsafe_allow_html=True)


elif page == "⚙️ Ingénierie des features":
    titre("Ingénierie des Features", "9 entrées brutes → 27 features production-ready", "⚙️")

    # Évolution des features
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(danger_box("""
            <h3 style='color: #dc3545; margin-top: 0;'>❌ Version 1 : Non-Production</h3>
            <div class='stat-number' style='color: #dc3545;'>50</div>
            <div class='stat-label'>Features avec historique</div>
            <hr style='margin: 15px 0;'>
            <h4>Problèmes :</h4>
            <ul class='custom-list'>
                <li>Dépendances à l'historique utilisateur (user_avg_amount, tx_count_1h, rolling stats)</li>
                <li>Impossible sans BDD temps réel</li>
                <li>Complexité de maintenance</li>
                <li>Latence élevée (requêtes DB)</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h3 style='color: #28a745; margin-top: 0;'>✅ Version 2 : Production-Ready</h3>
            <div class='stat-number' style='color: #28a745;'>27</div>
            <div class='stat-label'>Features stateless</div>
            <hr style='margin: 15px 0;'>
            <h4>Avantages :</h4>
            <ul class='custom-list'>
                <li><strong>Zéro historique</strong> requis</li>
                <li>Calcul instantané (transaction courante uniquement)</li>
                <li>API simple et rapide (~137ms)</li>
                <li>Performances maintenues : 93.5% accuracy</li>
            </ul>
        """), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Catégories de features
    st.markdown("<div class='section-header'>📦 5 Catégories de Features</div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #667eea;'>1️⃣ Features d'Origine (6 features)</h3>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <p style='font-size: 1.05rem;'>Colonnes brutes conservées telles quelles :</p>
        <ul class='custom-list'>
            <li><strong>step</strong> : Timestamp (heure dans le mois)</li>
            <li><strong>amount</strong> : Montant de la transaction</li>
            <li><strong>oldbalanceOrg</strong> : Solde avant (origine)</li>
            <li><strong>newbalanceOrig</strong> : Solde après (origine)</li>
            <li><strong>oldbalanceDest</strong> : Solde avant (destination)</li>
            <li><strong>newbalanceDest</strong> : Solde après (destination)</li>
        </ul>
        <p style='color: #666; margin-top: 10px;'><em>Base pour calculer les features dérivées</em></p>
    """), unsafe_allow_html=True)

    st.markdown("<h3 style='color: #764ba2;'>2️⃣ Features Montant (4 features)</h3>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <ul class='custom-list'>
            <li><strong>log_amount</strong> : log(amount + 1) pour normaliser distribution</li>
            <li><strong>amount_to_balance_ratio</strong> : amount / oldbalanceOrg (% du solde transféré)</li>
            <li><strong>exceeds_balance</strong> : 1 si amount > oldbalanceOrg (signal de fraude potentiel)</li>
            <li><strong>high_amount</strong> : 1 si amount > 200,000 (seuil flaggedFraud)</li>
        </ul>
        <p style='color: #0066cc; margin-top: 10px;'>
        <strong>💡 Insight :</strong> Les fraudes impliquent souvent des montants atypiques (très élevés ou ratio anormal).
        </p>
    """), unsafe_allow_html=True)

    st.markdown("<h3 style='color: #f093fb;'>3️⃣ Features Temporelles (4 features)</h3>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <ul class='custom-list'>
            <li><strong>is_night</strong> : 1 si transaction entre 0h-6h (patterns frauduleux nocturnes)</li>
            <li><strong>is_weekend</strong> : 1 si jour = samedi/dimanche (moins de monitoring)</li>
            <li><strong>hour_sin</strong> : sin(2π × heure/24) - encodage cyclique</li>
            <li><strong>hour_cos</strong> : cos(2π × heure/24) - encodage cyclique</li>
        </ul>
        <p style='color: #0066cc; margin-top: 10px;'>
        <strong>💡 Insight :</strong> Encodage sin/cos pour capturer la cyclicité (23h proche de 0h).
        </p>
    """), unsafe_allow_html=True)

    st.markdown("<h3 style='color: #4facfe;'>4️⃣ Features Dynamiques de Solde (7 features)</h3>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <ul class='custom-list'>
            <li><strong>orig_balance_diff</strong> : newbalanceOrig - oldbalanceOrg (variation attendue)</li>
            <li><strong>dest_balance_diff</strong> : newbalanceDest - oldbalanceDest</li>
            <li><strong>balance_inconsistency</strong> : |orig_diff + amount| (incohérence comptable)</li>
            <li><strong>dest_balance_increase</strong> : 1 si dest_diff > 0</li>
            <li><strong>orig_account_drained</strong> : 1 si newbalanceOrig = 0 (compte vidé)</li>
            <li><strong>zero_orig_balance_before</strong> : 1 si oldbalanceOrg = 0</li>
            <li><strong>zero_dest_balance_before</strong> : 1 si oldbalanceDest = 0</li>
        </ul>
        <p style='color: #dc3545; margin-top: 10px;'>
        <strong>🚨 Fraude typique :</strong> Incohérences (balance_inconsistency élevée) ou compte vidé (orig_account_drained=1).
        </p>
    """), unsafe_allow_html=True)

    st.markdown("<h3 style='color: #00f2fe;'>5️⃣ Features Type & Compte (6 features)</h3>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <ul class='custom-list'>
            <li><strong>type_TRANSFER</strong> : 1 si type = TRANSFER</li>
            <li><strong>type_CASH_OUT</strong> : 1 si type = CASH_OUT</li>
            <li><strong>risky_type</strong> : 1 si TRANSFER ou CASH_OUT (99% des fraudes)</li>
            <li><strong>is_merchant_dest</strong> : 1 si destination commence par 'M' (marchand)</li>
            <li><strong>is_customer_to_customer</strong> : 1 si origine 'C' et destination 'C'</li>
            <li><strong>risk_score</strong> : Somme pondérée (risky_type + high_amount + exceeds_balance + inconsistency)</li>
        </ul>
        <p style='color: #dc3545; margin-top: 10px;'>
        <strong>🚨 Clé :</strong> <span class='highlight'>risky_type</span> capture 99% des fraudes (TRANSFER/CASH_OUT uniquement).
        </p>
    """), unsafe_allow_html=True)

    # Tableau récapitulatif
    st.markdown("<div class='section-header'>📊 Récapitulatif des 27 Features</div>", unsafe_allow_html=True)
    
    df_features = pd.DataFrame({
        'Catégorie': ['Origine', 'Montant', 'Temps', 'Soldes', 'Type/Compte', 'TOTAL'],
        'Nombre': [6, 4, 4, 7, 6, 27],
        'Calculable en Prod': ['✅', '✅', '✅', '✅', '✅', '✅'],
        'Dépendance Historique': ['❌', '❌', '❌', '❌', '❌', '❌'],
    })
    
    st.dataframe(df_features, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Impact
    st.markdown("<div class='section-header'>🎯 Impact & Bénéfices</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>✅ Production</h4>
            <p style='font-size: 1.05rem;'>
            <strong>Stateless :</strong> Aucune dépendance BDD<br>
            <strong>Latence :</strong> ~137ms (calcul instantané)<br>
            <strong>Scalable :</strong> API horizontalement scalable
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>📈 Performance</h4>
            <p style='font-size: 1.05rem;'>
            <strong>Accuracy :</strong> 93.5%<br>
            <strong>Rappel fraude :</strong> 87.1%<br>
            <strong>ROC-AUC :</strong> 98.2%
            </p>
        """), unsafe_allow_html=True)
    
    with col3:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🛠️ Maintenance</h4>
            <p style='font-size: 1.05rem;'>
            <strong>Complexité :</strong> Faible<br>
            <strong>Tests :</strong> Unitaires simples<br>
            <strong>Évolution :</strong> Ajout facile de features
            </p>
        """), unsafe_allow_html=True)


elif page == "🤖 Modèle Autoencoder":
    titre("Modèle Autoencoder", "Détection d'anomalies par reconstruction", "🤖")

    # Principe
    st.markdown("<div class='section-header'>🧠 Principe de l'Autoencoder</div>", unsafe_allow_html=True)
    st.markdown(info_box("""
        <p style='font-size: 1.15rem; line-height: 1.8;'>
        Un <strong>Autoencoder</strong> est un réseau de neurones qui apprend à <span class='highlight'>compresser puis reconstruire</span> 
        ses données d'entrée. Entraîné <strong>uniquement sur transactions normales</strong>, il apprend à reconnaître 
        les patterns légitimes.
        </p>
        <p style='font-size: 1.15rem; line-height: 1.8; margin-top: 15px;'>
        <strong>🔍 Détection d'anomalies :</strong><br>
        ✅ Transaction normale → Reconstruction fidèle → <strong>Erreur faible</strong><br>
        🚨 Transaction frauduleuse → Pattern inconnu → <strong>Erreur élevée</strong> → ALERTE
        </p>
        <p style='font-size: 1.05rem; color: #666; margin-top: 15px;'>
        <em>Pas besoin d'exemples de fraudes pour l'entraînement : apprentissage non-supervisé.</em>
        </p>
    """), unsafe_allow_html=True)

    # Architecture visuelle
    st.markdown("<div class='section-header'>🏗️ Architecture du Réseau</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
                <div style='text-align: center; font-size: 1.2rem; margin-bottom: 20px; color: #667eea; font-weight: 600;'>
                    🔄 Flow de l'Autoencoder
                </div>
                <div style='display: flex; align-items: center; justify-content: space-between; margin: 20px 0;'>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
                        padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>INPUT</strong><br>27 features
                        </div>
                    </div>
                    <div style='font-size: 2rem; padding: 0 10px;'>→</div>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: #764ba2; color: white; padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>Dense</strong><br>64 neurons
                        </div>
                    </div>
                    <div style='font-size: 2rem; padding: 0 10px;'>→</div>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: #8e54e9; color: white; padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>Dense</strong><br>32 neurons
                        </div>
                    </div>
                </div>
                <div style='text-align: center; margin: 25px 0;'>
                    <div style='display: inline-block; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); 
                    color: white; padding: 20px 40px; border-radius: 15px; font-weight: 700; font-size: 1.3rem;
                    box-shadow: 0 6px 20px rgba(255,107,107,0.3);'>
                        ⚡ BOTTLENECK<br>
                        <span style='font-size: 2rem;'>16</span> neurons
                    </div>
                </div>
                <div style='display: flex; align-items: center; justify-content: space-between; margin: 20px 0;'>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: #8e54e9; color: white; padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>Dense</strong><br>32 neurons
                        </div>
                    </div>
                    <div style='font-size: 2rem; padding: 0 10px;'>→</div>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: #764ba2; color: white; padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>Dense</strong><br>64 neurons
                        </div>
                    </div>
                    <div style='font-size: 2rem; padding: 0 10px;'>→</div>
                    <div style='text-align: center; flex: 1;'>
                        <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; 
                        padding: 15px; border-radius: 10px; margin: 5px;'>
                            <strong>OUTPUT</strong><br>27 features
                        </div>
                    </div>
                </div>
                <div style='text-align: center; margin-top: 25px; padding: 15px; background: #f8f9fa; border-radius: 10px;'>
                    <strong style='color: #dc3545;'>📊 Erreur de Reconstruction</strong><br>
                    <span style='font-size: 1.1rem;'>MSE(Input, Output) → Seuil 0.304</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Spécifications techniques
    st.markdown("<div class='section-header'>⚙️ Spécifications Techniques</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🏗️ Architecture</h4>
            <ul class='custom-list'>
                <li><strong>Input Layer :</strong> 27 features</li>
                <li><strong>Encoder :</strong>
                    <ul>
                        <li>Dense(64, relu, L2=0.001)</li>
                        <li>Dense(32, relu, L2=0.001)</li>
                        <li>Dense(16, relu) - Bottleneck</li>
                    </ul>
                </li>
                <li><strong>Decoder :</strong>
                    <ul>
                        <li>Dense(32, relu)</li>
                        <li>Dense(64, relu)</li>
                        <li>Dense(27, linear) - Output</li>
                    </ul>
                </li>
            </ul>
        """), unsafe_allow_html=True)
        
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>📊 Paramètres</h4>
            <p style='font-size: 1.1rem;'>
            <strong>Total paramètres :</strong> 9,579<br>
            <strong>Taille modèle :</strong> ~40 KB (léger)<br>
            <strong>Temps inférence :</strong> &lt;10ms<br>
            <strong>Régularisation :</strong> L2 (0.001)
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🎓 Entraînement</h4>
            <ul class='custom-list'>
                <li><strong>Données :</strong> Transactions normales uniquement (83.57% du dataset)</li>
                <li><strong>Loss :</strong> Mean Squared Error (MSE)</li>
                <li><strong>Optimizer :</strong> Adam</li>
                <li><strong>Batch size :</strong> 256</li>
                <li><strong>Epochs :</strong> 100 (early stopping)</li>
                <li><strong>Validation split :</strong> 20%</li>
            </ul>
        """), unsafe_allow_html=True)
        
        st.markdown(warning_box("""
            <h4 style='color: #ff6b6b; margin-top: 0;'>🎯 Seuil de Détection</h4>
            <p style='font-size: 1.1rem;'>
            <strong>Méthode :</strong> 95e percentile des erreurs normales<br>
            <strong>Valeur :</strong> ~0.304<br>
            <strong>Logique :</strong> Erreur > 0.304 → FRAUDE<br>
            <strong>Justification :</strong> Compromis précision/rappel optimal
            </p>
        """), unsafe_allow_html=True)

    # Avantages
    st.markdown("<div class='section-header'>✅ Pourquoi l'Autoencoder ?</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🎯</div>
                <h4 style='color: #667eea;'>Non-Supervisé</h4>
                <p style='font-size: 1rem; line-height: 1.7; color: #1a1a1a;'>
                Pas besoin d'exemples de fraudes étiquetés pour l'entraînement. 
                Apprend la distribution normale.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🔍</div>
                <h4 style='color: #667eea;'>Anomalies Inconnues</h4>
                <p style='font-size: 1rem; line-height: 1.7; color: #1a1a1a;'>
                Détecte toute déviation du comportement normal, 
                même les nouveaux types de fraude.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>⚡</div>
                <h4 style='color: #667eea;'>Léger & Rapide</h4>
                <p style='font-size: 1rem; line-height: 1.7; color: #1a1a1a;'>
                9,579 paramètres seulement. 
                Inférence ultra-rapide (&lt;10ms).
                </p>
            </div>
        """, unsafe_allow_html=True)


elif page == "🎯 API de prédiction":
    titre("API de Prédiction", "FastAPI - Temps réel en production", "🎯")

    # Métriques clés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(metric_card("Latence", "~137ms", "⚡"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Port", "8000", "🔌"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Endpoints", "2", "📡"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Format", "JSON", "📄"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Flux de prédiction
    st.markdown("<div class='section-header'>🔄 Flux de Prédiction</div>", unsafe_allow_html=True)
    
    flow_steps = [
        ("1. Requête POST /predict", "9 champs bruts envoyés (step, type, amount, balances...)", "#667eea"),
        ("2. Transformation Features", "9 entrées → 27 features calculées (montant, temps, soldes, type)", "#764ba2"),
        ("3. Normalisation", "StandardScaler pré-entraîné (fit sur train set)", "#8e54e9"),
        ("4. Prédiction Autoencoder", "Passage dans le modèle : Input(27) → Reconstruction(27)", "#f093fb"),
        ("5. Calcul Erreur MSE", "reconstruction_error = mean((input - output)²)", "#4facfe"),
        ("6. Décision", "Erreur > 0.304 → FRAUDE | Sinon → NORMAL", "#00f2fe"),
        ("7. Log & Alerte", "Enregistrement JSONL + Email SMTP si fraude détectée", "#43e97b"),
        ("8. Réponse JSON", "is_fraud, reconstruction_error, threshold, confidence, timestamp", "#38f9d7"),
    ]
    
    for step, desc, color in flow_steps:
        st.markdown(f"""
            <div class='timeline-item' style='border-left-color: {color};'>
                <h4 style='color: {color}; margin: 0;'>{step}</h4>
                <p style='margin: 5px 0 0 0; font-size: 1.05rem;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    # Endpoints
    st.markdown("<div class='section-header'>📡 Endpoints Disponibles</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(success_box("""
            <h3 style='color: #28a745; margin-top: 0;'>POST /predict</h3>
            <p style='font-size: 1.05rem;'><strong>Description :</strong> Prédiction de fraude sur une transaction</p>
            <h4>Payload JSON (9 champs) :</h4>
            <ul class='custom-list' style='font-size: 0.95rem;'>
                <li><strong>step</strong> : int (heure)</li>
                <li><strong>type</strong> : str (PAYMENT, TRANSFER, CASH_OUT, CASH_IN, DEBIT)</li>
                <li><strong>amount</strong> : float</li>
                <li><strong>nameOrig</strong> : str (compte origine)</li>
                <li><strong>oldbalanceOrg</strong> : float</li>
                <li><strong>newbalanceOrig</strong> : float</li>
                <li><strong>nameDest</strong> : str (compte destination)</li>
                <li><strong>oldbalanceDest</strong> : float</li>
                <li><strong>newbalanceDest</strong> : float</li>
            </ul>
            <p style='margin-top: 10px; font-size: 0.9rem; color: #666;'>
            <em>Note : isFraud et isFlaggedFraud ne sont PAS requis (prédiction only)</em>
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h3 style='color: #0066cc; margin-top: 0;'>GET /health</h3>
            <p style='font-size: 1.05rem;'><strong>Description :</strong> Health check du service</p>
            <h4>Réponse :</h4>
            <pre style='background: #f5f5f5; padding: 15px; border-radius: 8px; overflow-x: auto;'>
{
  "status": "healthy",
  "model_loaded": true,
  "scaler_loaded": true,
  "threshold": 0.304
}
            </pre>
            <p style='margin-top: 15px; font-size: 1.05rem;'>
            <strong>Usage :</strong> Docker Compose healthcheck + monitoring
            </p>
        """), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Exemple réponse
    st.markdown("<div class='section-header'>📄 Exemple de Réponse</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(danger_box("""
            <h4 style='color: #dc3545; margin-top: 0;'>🚨 Cas : Fraude Détectée</h4>
            <pre style='background: #fff; padding: 15px; border-radius: 8px; overflow-x: auto; border: 1px solid #ddd;'>
{
  "is_fraud": true,
  "reconstruction_error": 0.512,
  "threshold": 0.304,
  "confidence": 0.85,
  "timestamp": "2026-01-16T14:23:45",
  "alert_sent": true
}
            </pre>
            <p style='margin-top: 10px; font-size: 1rem;'>
            ✅ Alerte email envoyée immédiatement<br>
            ✅ Log enregistré dans <code>metrics/api_metrics.jsonl</code>
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>✅ Cas : Transaction Normale</h4>
            <pre style='background: #fff; padding: 15px; border-radius: 8px; overflow-x: auto; border: 1px solid #ddd;'>
{
  "is_fraud": false,
  "reconstruction_error": 0.187,
  "threshold": 0.304,
  "confidence": 0.92,
  "timestamp": "2026-01-16T14:24:12",
  "alert_sent": false
}
            </pre>
            <p style='margin-top: 10px; font-size: 1rem;'>
            ✅ Transaction approuvée<br>
            ✅ Log enregistré (pas d'alerte)
            </p>
        """), unsafe_allow_html=True)

    # Performance
    st.markdown("<div class='section-header'>⚡ Performance & Observabilité</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>⚡</div>
                <h4 style='color: #667eea;'>Latence</h4>
                <p style='font-size: 1.05rem; line-height: 1.7; color: #1a1a1a;'>
                <strong>Moyenne :</strong> ~137ms<br>
                <strong>P95 :</strong> ~180ms<br>
                <strong>Max :</strong> ~250ms
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>📊</div>
                <h4 style='color: #667eea;'>Logging</h4>
                <p style='font-size: 1.05rem; line-height: 1.7; color: #1a1a1a;'>
                <strong>Format :</strong> JSONL<br>
                <strong>Fichier :</strong> api_metrics.jsonl<br>
                <strong>Champs :</strong> 15+ métriques
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🛡️</div>
                <h4 style='color: #667eea;'>Robustesse</h4>
                <p style='font-size: 1.05rem; line-height: 1.7; color: #1a1a1a;'>
                <strong>Validation :</strong> Pydantic<br>
                <strong>Errors :</strong> HTTP 422<br>
                <strong>Health :</strong> /health endpoint
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(warning_box("""
        <h4 style='margin-top: 0;'>🚀 Commandes Utiles</h4>
        <p style='font-size: 1.05rem;'>
        <strong>Lancer l'API :</strong> <code>docker-compose up fraud-api</code> ou <code>uvicorn api.main:app --port 8000</code><br>
        <strong>Tester :</strong> <code>curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @sample.json</code><br>
        <strong>Health check :</strong> <code>curl http://localhost:8000/health</code>
        </p>
    """), unsafe_allow_html=True)


elif page == "🐳 Docker & MLOps":
    titre("Docker & MLOps", "Architecture microservices conteneurisée", "🐳")

    # Architecture
    st.markdown("<div class='section-header'>🏗️ Architecture Microservices</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: white; padding: 30px; border-radius: 15px; box-shadow: 0 6px 16px rgba(0,0,0,0.1); margin: 20px 0;'>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: start;'>
                <div>
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; 
                    padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px;'>
                        <h3 style='margin: 0; font-size: 1.8rem;'>🚀 fraud-api</h3>
                        <p style='margin: 10px 0 0 0; font-size: 1.1rem;'>Service de Prédiction</p>
                    </div>
                    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Port :</strong> 8000</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Framework :</strong> FastAPI</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Endpoint :</strong> POST /predict</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Charge :</strong> Modèle, Scaler, Threshold</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Alertes :</strong> SMTP intégré</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Logs :</strong> api_metrics.jsonl</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Health :</strong> GET /health</p>
                    </div>
                </div>
                <div>
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; 
                    padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px;'>
                        <h3 style='margin: 0; font-size: 1.8rem;'>📊 fraud-dashboard</h3>
                        <p style='margin: 10px 0 0 0; font-size: 1.1rem;'>Monitoring & Analytics</p>
                    </div>
                    <div style='background: #f8f9fa; padding: 20px; border-radius: 10px;'>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Port :</strong> 8501</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Framework :</strong> Streamlit</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Pages :</strong> 5 (Overview, Analytics, Perf, Live, Business)</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Source :</strong> Lecture JSONL</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Refresh :</strong> Temps réel (5s)</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Visualisations :</strong> Plotly, Altair</p>
                        <p style='margin: 5px 0; color: #1a1a1a;'><strong>Metrics :</strong> KPI, distributions, tendances</p>
                    </div>
                </div>
            </div>
            <div style='text-align: center; margin-top: 30px; padding: 20px; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
            border-radius: 10px;'>
                <p style='margin: 0; font-size: 1.2rem; font-weight: 600;'>🔗 Réseau Docker partagé : <code>fraud-detection-network</code></p>
                <p style='margin: 5px 0 0 0; color: #666;'>Communication inter-services + isolation</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Volumes
    st.markdown("<div class='section-header'>💾 Volumes Persistants</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>📦 ./models</h4>
            <p style='font-size: 1.05rem; color: #1a1a1a;'>
            <strong>Contenu :</strong><br>
            - autoencoder.keras<br>
            - encoder.keras<br>
            - scaler.pkl<br>
            - ae_threshold.npy
            </p>
            <p style='margin-top: 10px; color: #666;'><em>Partagé entre API et dashboard</em></p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>📊 ./metrics</h4>
            <p style='font-size: 1.05rem; color: #1a1a1a;'>
            <strong>Contenu :</strong><br>
            - api_metrics.jsonl<br>
            - logs système
            </p>
            <p style='margin-top: 10px; color: #666;'><em>Logs temps réel consommés par dashboard</em></p>
        """), unsafe_allow_html=True)
    
    with col3:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🗂️ ./data</h4>
            <p style='font-size: 1.05rem; color: #1a1a1a;'>
            <strong>Contenu :</strong><br>
            - paysim_test.csv<br>
            - features lists
            </p>
            <p style='margin-top: 10px; color: #666;'><em>Optionnel : datasets pour tests</em></p>
        """), unsafe_allow_html=True)

    # Fichiers de configuration
    st.markdown("<div class='section-header'>⚙️ Fichiers de Configuration</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>📄 Dockerfile</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Base image :</strong> python:3.10-slim<br>
            <strong>Dépendances :</strong> requirements.txt<br>
            <strong>Ports exposés :</strong> 8000 (API), 8501 (Dashboard)<br>
            <strong>Workdir :</strong> /app<br>
            <strong>Entrypoint :</strong> Configurable (uvicorn ou streamlit)
            </p>
            <h5 style='margin-top: 15px; color: #1a1a1a;'>Optimisations :</h5>
            <ul style='font-size: 0.95rem; color: #1a1a1a;'>
                <li>Multi-stage build (future)</li>
                <li>Layer caching efficace</li>
                <li>.dockerignore (tests, docs)</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🐳 docker-compose.yml</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Version :</strong> 3.8<br>
            <strong>Services :</strong> fraud-api, fraud-dashboard<br>
            <strong>Réseau :</strong> fraud-detection-network (bridge)<br>
            <strong>Restart policy :</strong> unless-stopped<br>
            <strong>Variables :</strong> .env file
            </p>
            <h5 style='margin-top: 15px; color: #1a1a1a;'>Features :</h5>
            <ul style='font-size: 0.95rem; color: #1a1a1a;'>
                <li>Healthchecks (GET /health)</li>
                <li>Depends_on avec conditions</li>
                <li>Volumes bind mounts</li>
            </ul>
        """), unsafe_allow_html=True)

    st.markdown(warning_box("""
        <h4 style='margin-top: 0; color: #1a1a1a;'>🔐 .env (Variables d'Environnement)</h4>
        <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
        <strong>ALERT_ENABLED :</strong> true/false (activer alertes)<br>
        <strong>SMTP_SERVER :</strong> smtp.gmail.com<br>
        <strong>SMTP_PORT :</strong> 587<br>
        <strong>SENDER_EMAIL :</strong> votre_email@gmail.com<br>
        <strong>SENDER_PASSWORD :</strong> mot_de_passe_application<br>
        <strong>RECIPIENT_EMAIL :</strong> destinataire@entreprise.com
        </p>
        <p style='margin-top: 10px; color: #666;'>
        <em>⚠️ Ne jamais commiter .env (ajouté dans .gitignore)</em>
        </p>
    """), unsafe_allow_html=True)

    # Pratiques MLOps
    st.markdown("<div class='section-header'>✅ Bonnes Pratiques MLOps</div>", unsafe_allow_html=True)
    
    practices = [
        ("🏥 Health Checks", "Endpoint /health vérifié toutes les 30s. Redémarrage auto si échec."),
        ("🔄 Restart Policy", "unless-stopped : redémarrage automatique sauf arrêt manuel."),
        ("📦 Volumes Persistants", "Modèles, logs et métriques préservés entre redémarrages."),
        ("🔐 Secrets Management", "Variables sensibles dans .env (hors Git). Support Docker secrets (future)."),
        ("🌐 Réseau Isolé", "Services communiquent via réseau Docker privé."),
        ("📊 Observabilité", "Logs JSONL structurés + dashboard temps réel."),
        ("⚡ Performance", "Image slim (Python 3.10) + caching layers."),
        ("🧪 Reproductibilité", "requirements.txt versionné + seed fixe."),
    ]
    
    for title, desc in practices:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%); padding: 15px 20px; 
            border-radius: 10px; margin: 10px 0; border-left: 4px solid #00acc1;'>
                <h4 style='margin: 0; color: #00695c;'>{title}</h4>
                <p style='margin: 5px 0 0 0; font-size: 1.05rem; color: #004d40;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(success_box("""
        <h4 style='margin-top: 0;'>🚀 Commandes Docker Compose</h4>
        <p style='font-size: 1.05rem; line-height: 2;'>
        <strong>Démarrer :</strong> <code>docker-compose up -d</code><br>
        <strong>Arrêter :</strong> <code>docker-compose down</code><br>
        <strong>Logs API :</strong> <code>docker-compose logs -f fraud-api</code><br>
        <strong>Logs Dashboard :</strong> <code>docker-compose logs -f fraud-dashboard</code><br>
        <strong>Rebuild :</strong> <code>docker-compose up --build</code><br>
        <strong>Status :</strong> <code>docker-compose ps</code>
        </p>
    """), unsafe_allow_html=True)


elif page == "📊 Tableau de bord":
    titre("Tableau de Bord Monitoring", "5 pages Streamlit pour monitoring complet", "📊")

    # Vue d'ensemble
    st.markdown("<div class='section-header'>🎯 Vue d'Ensemble du Dashboard</div>", unsafe_allow_html=True)
    
    st.markdown(info_box("""
        <p style='font-size: 1.15rem; line-height: 1.8;'>
        Dashboard Streamlit multi-pages conçu pour le <strong>monitoring opérationnel</strong> du système 
        de détection de fraude. Consomme les métriques JSONL générées par l'API en temps réel.
        </p>
        <p style='font-size: 1.1rem; margin-top: 15px;'>
        <strong>Port :</strong> 8501 | <strong>Framework :</strong> Streamlit | <strong>Refresh :</strong> 5 secondes (page Temps Réel)
        </p>
    """), unsafe_allow_html=True)

    st.markdown("<div class='section-header'>📚 Les 5 Pages du Dashboard</div>", unsafe_allow_html=True)

    # Page 1 : Overview
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; 
        border-radius: 12px; margin: 15px 0; color: white;'>
            <h3 style='margin: 0;'>1️⃣ Vue d'Ensemble</h3>
            <p style='margin: 10px 0; font-size: 1.1rem; line-height: 1.7;'>
            Tableau de bord principal avec KPI essentiels :
            </p>
            <ul style='font-size: 1.05rem; line-height: 1.8;'>
                <li><strong>Volumes :</strong> Total transactions, taux de fraude actuel</li>
                <li><strong>Performance :</strong> Temps de réponse moyen, P95, max</li>
                <li><strong>Tendances :</strong> Évolution du taux de fraude (graphique temporel)</li>
                <li><strong>Distribution types :</strong> Pie chart TRANSFER/CASH_OUT/PAYMENT...</li>
                <li><strong>Top montants :</strong> Transactions les plus élevées</li>
            </ul>
            <p style='margin-top: 10px; font-size: 1rem; opacity: 0.9;'>
            🎯 <em>Usage : Monitoring quotidien, réunions d'équipe</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Page 2 : Deep Analytics
    st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; 
        border-radius: 12px; margin: 15px 0; color: white;'>
            <h3 style='margin: 0;'>2️⃣ Deep Analytics</h3>
            <p style='margin: 10px 0; font-size: 1.1rem; line-height: 1.7;'>
            Analyses avancées des distributions et patterns :
            </p>
            <ul style='font-size: 1.05rem; line-height: 1.8;'>
                <li><strong>Distributions erreurs :</strong> Histogrammes normales vs fraudes</li>
                <li><strong>Patterns temporels :</strong> Fraudes par heure/jour (heatmap)</li>
                <li><strong>Montants :</strong> Box plots, outliers</li>
                <li><strong>Soldes :</strong> Analyse incohérences, drains de compte</li>
                <li><strong>Corrélations :</strong> Features vs fraude (correlation matrix)</li>
            </ul>
            <p style='margin-top: 10px; font-size: 1rem; opacity: 0.9;'>
            🔍 <em>Usage : Investigations approfondies, tuning modèle</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Page 3 : Performance Modèle
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; 
        border-radius: 12px; margin: 15px 0; color: white;'>
            <h3 style='margin: 0;'>3️⃣ Performance Modèle</h3>
            <p style='margin: 10px 0; font-size: 1.1rem; line-height: 1.7;'>
            Métriques ML détaillées (nécessite ground truth) :
            </p>
            <ul style='font-size: 1.05rem; line-height: 1.8;'>
                <li><strong>Matrice de confusion :</strong> TP, TN, FP, FN (heatmap)</li>
                <li><strong>Métriques :</strong> Accuracy, Précision, Rappel, F1-score</li>
                <li><strong>ROC Curve :</strong> AUC, seuil optimal</li>
                <li><strong>Precision-Recall Curve :</strong> Trade-off visualisé</li>
                <li><strong>Calibration :</strong> Vérification confiance vs taux réel</li>
            </ul>
            <p style='margin-top: 10px; font-size: 1rem; opacity: 0.9;'>
            🎯 <em>Usage : Validation modèle, ajustement seuil</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Page 4 : Temps Réel
    st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 25px; 
        border-radius: 12px; margin: 15px 0; color: white;'>
            <h3 style='margin: 0;'>4️⃣ Monitoring Temps Réel</h3>
            <p style='margin: 10px 0; font-size: 1.1rem; line-height: 1.7;'>
            Surveillance live des dernières transactions :
            </p>
            <ul style='font-size: 1.05rem; line-height: 1.8;'>
                <li><strong>Dernières 10 minutes :</strong> Stream de transactions</li>
                <li><strong>Auto-refresh :</strong> Toutes les 5 secondes</li>
                <li><strong>Alertes visuelles :</strong> Red highlight si fraude</li>
                <li><strong>Détails :</strong> Timestamp, type, montant, erreur, décision</li>
                <li><strong>Graphique live :</strong> Évolution erreurs en temps réel</li>
            </ul>
            <p style='margin-top: 10px; font-size: 1rem; opacity: 0.9;'>
            🟢 <em>Usage : Monitoring 24/7, war room, incidents</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Page 5 : Business
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 25px; 
        border-radius: 12px; margin: 15px 0; color: #333;'>
            <h3 style='margin: 0; color: #d63031;'>5️⃣ Impact Business</h3>
            <p style='margin: 10px 0; font-size: 1.1rem; line-height: 1.7;'>
            KPI métier et ROI du système :
            </p>
            <ul style='font-size: 1.05rem; line-height: 1.8;'>
                <li><strong>Montants frauduleux bloqués :</strong> Somme des TP × amount</li>
                <li><strong>Types à risque :</strong> Classement TRANSFER/CASH_OUT</li>
                <li><strong>Coûts évités :</strong> Estimation pertes prévenues</li>
                <li><strong>Faux positifs :</strong> Impact user experience</li>
                <li><strong>Recommandations :</strong> Actions pour réduire FP sans dégrader rappel</li>
            </ul>
            <p style='margin-top: 10px; font-size: 1rem;'>
            💰 <em>Usage : Reporting exec, justification investissement</em>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Technologies & Visualisations
    st.markdown("<div class='section-header'>🎨 Technologies & Visualisations</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🛠️ Stack Technique</h4>
            <ul class='custom-list'>
                <li><strong>Streamlit :</strong> Framework UI interactif</li>
                <li><strong>Plotly :</strong> Graphiques interactifs (hover, zoom)</li>
                <li><strong>Altair :</strong> Graphiques déclaratifs</li>
                <li><strong>Pandas :</strong> Manipulation données JSONL</li>
                <li><strong>Scikit-learn :</strong> Métriques ML (confusion_matrix, roc_curve...)</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>📊 Types de Visualisations</h4>
            <ul class='custom-list'>
                <li><strong>Metric cards :</strong> KPI avec deltas</li>
                <li><strong>Line charts :</strong> Tendances temporelles</li>
                <li><strong>Bar charts :</strong> Distributions catégorielles</li>
                <li><strong>Heatmaps :</strong> Matrice confusion, corrélations</li>
                <li><strong>Box plots :</strong> Distributions avec outliers</li>
                <li><strong>Tables interactives :</strong> Filtres, tri, recherche</li>
            </ul>
        """), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(warning_box("""
        <h4 style='margin-top: 0;'>🚀 Accès au Dashboard</h4>
        <p style='font-size: 1.1rem; line-height: 1.8;'>
        <strong>URL locale :</strong> <code>http://localhost:8501</code><br>
        <strong>Lancer :</strong> <code>docker-compose up fraud-dashboard</code> ou <code>streamlit run monitoring/app.py</code><br>
        <strong>Navigation :</strong> Menu latéral gauche (5 pages)<br>
        <strong>Refresh :</strong> Automatique (page Temps Réel) ou manuel (bouton R)
        </p>
    """), unsafe_allow_html=True)


elif page == "📧 Alertes email":
    titre("Alertes Email", "Notifications SMTP en temps réel", "📧")

    # Principe
    st.markdown("<div class='section-header'>✉️ Principe des Alertes</div>", unsafe_allow_html=True)
    
    st.markdown(info_box("""
        <p style='font-size: 1.15rem; line-height: 1.8; color: #1a1a1a;'>
        Chaque fois qu'une <strong>fraude est détectée</strong> (erreur reconstruction > seuil 0.304), 
        l'API envoie automatiquement un <strong>email HTML formaté</strong> aux équipes métiers via SMTP.
        </p>
        <p style='font-size: 1.1rem; margin-top: 15px; color: #1a1a1a;'>
        <strong>⏱️ Latence :</strong> 2-3 secondes entre détection et réception email<br>
        <strong>📧 Format :</strong> HTML avec tableaux, couleurs, métadonnées complètes<br>
        <strong>🛡️ Sécurité :</strong> Mot de passe application (Google) ou SMTP dédié
        </p>
    """), unsafe_allow_html=True)

    # Configuration SMTP
    st.markdown("<div class='section-header'>⚙️ Configuration SMTP (.env)</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(warning_box("""
            <h4 style='color: #ff6b6b; margin-top: 0;'>📝 Variables Requises</h4>
            <pre style='background: #fff; padding: 15px; border-radius: 8px; border: 1px solid #ddd; font-size: 0.95rem; color: #1a1a1a;'>
ALERT_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=votre_email@gmail.com
SENDER_PASSWORD=votre_mot_de_passe_app
RECIPIENT_EMAIL=equipe@entreprise.com
            </pre>
            <p style='margin-top: 10px; font-size: 1rem; color: #666;'>
            <em>⚠️ Utiliser un mot de passe d'application (pas le mot de passe Gmail principal)</em>
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #0066cc; margin-top: 0;'>🛠️ Providers SMTP Courants</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Gmail :</strong><br>
            - Server: smtp.gmail.com<br>
            - Port: 587 (TLS)<br>
            - Requète : Mot de passe d'application<br>
            <br>
            <strong>Outlook :</strong><br>
            - Server: smtp-mail.outlook.com<br>
            - Port: 587<br>
            <br>
            <strong>SendGrid/Mailgun :</strong><br>
            - Serveurs dédiés entreprise<br>
            - API keys disponibles
            </p>
        """), unsafe_allow_html=True)

    # Template Email
    st.markdown("<div class='section-header'>📬 Template Email (Exemple)</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
        border: 3px solid #dc3545; margin: 20px 0;'>
            <div style='background: linear-gradient(135deg, #dc3545 0%, #c92a2a 100%); color: white; 
            padding: 20px; margin: -25px -25px 20px -25px; border-radius: 9px 9px 0 0;'>
                <h2 style='margin: 0; font-size: 1.8rem;'>🚨 ALERTE FRAUDE DÉTECTÉE</h2>
                <p style='margin: 5px 0 0 0; font-size: 1.1rem;'>Système de Détection MLOps</p>
            </div>
            <div style='padding: 20px; background: #fff5f5; border-radius: 8px; margin: 15px 0;'>
                <p style='font-size: 1.1rem; margin: 0; color: #dc3545; font-weight: 600;'>
                ⚠️ Une transaction frauduleuse vient d'être identifiée par le modèle Autoencoder.
                </p>
            </div>
            <h3 style='color: #333; margin-top: 25px; border-bottom: 2px solid #eee; padding-bottom: 10px;'>
            📊 Détails de la Transaction
            </h3>
            <table style='width: 100%; border-collapse: collapse; margin: 15px 0; color: #1a1a1a;'>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Type</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #1a1a1a;'>TRANSFER</td>
                </tr>
                <tr>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Montant</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #dc3545; font-weight: 700;'>352,487.50 €</td>
                </tr>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Compte Origine</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #1a1a1a;'>C1234567890</td>
                </tr>
                <tr>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Compte Destination</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #1a1a1a;'>C9876543210</td>
                </tr>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Timestamp</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #1a1a1a;'>2026-01-16 14:23:45</td>
                </tr>
            </table>
            <h3 style='color: #333; margin-top: 25px; border-bottom: 2px solid #eee; padding-bottom: 10px;'>
            🤖 Scoring Modèle
            </h3>
            <table style='width: 100%; border-collapse: collapse; margin: 15px 0; color: #1a1a1a;'>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Erreur Reconstruction</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #dc3545; font-weight: 700;'>0.512</td>
                </tr>
                <tr>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Seuil Détection</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #1a1a1a;'>0.304</td>
                </tr>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 12px; border: 1px solid #ddd; font-weight: 600; color: #1a1a1a;'>Confiance</td>
                    <td style='padding: 12px; border: 1px solid #ddd; color: #28a745; font-weight: 700;'>85%</td>
                </tr>
            </table>
            <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 15px; 
            border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff6b6b;'>
                <p style='margin: 0; font-size: 1.05rem; color: #333;'>
                <strong>🛠️ Actions Recommandées :</strong><br>
                1. Bloquer temporairement le compte origine<br>
                2. Vérifier l'historique des transactions similaires<br>
                3. Contacter le client pour confirmation
                </p>
            </div>
            <p style='text-align: center; color: #999; font-size: 0.9rem; margin-top: 25px; border-top: 1px solid #eee; padding-top: 15px;'>
            🤖 Email automatique généré par le système MLOps Fraud Detection<br>
            Ne pas répondre à cet email
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Workflow
    st.markdown("<div class='section-header'>🔄 Workflow d'Alerte</div>", unsafe_allow_html=True)
    
    workflow_steps = [
        ("1. Détection Fraude", "API : reconstruction_error > 0.304", "#dc3545"),
        ("2. Préparation Email", "Génération HTML avec données transaction + scoring", "#ff6b6b"),
        ("3. Connexion SMTP", "TLS sur port 587 (Gmail/Outlook)", "#764ba2"),
        ("4. Envoi", "smtplib.sendmail() avec timeout 10s", "#667eea"),
        ("5. Log", "Enregistrement status envoi dans api_metrics.jsonl", "#4facfe"),
        ("6. Réception", "Équipe métiers reçoit email sous 2-3s", "#28a745"),
    ]
    
    for step, desc, color in workflow_steps:
        st.markdown(f"""
            <div style='border-left: 4px solid {color}; padding: 15px 20px; margin: 10px 0; 
            background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.05);'>
                <h4 style='margin: 0; color: {color};'>{step}</h4>
                <p style='margin: 5px 0 0 0; font-size: 1.05rem; color: #1a1a1a;'>{desc}</p>
            </div>
        """, unsafe_allow_html=True)

    # Troubleshooting
    st.markdown("<div class='section-header'>🔧 Troubleshooting</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(danger_box("""
            <h4 style='color: #dc3545; margin-top: 0;'>❌ Erreurs Courantes</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>SMTPAuthenticationError :</strong><br>
            → Vérifier mot de passe application (pas mdp Gmail principal)<br>
            → Activer "Accès applications moins sécurisées" (Gmail)<br>
            <br>
            <strong>TimeoutError :</strong><br>
            → Vérifier firewall/proxy<br>
            → Essayer port 465 (SSL) au lieu de 587 (TLS)<br>
            <br>
            <strong>ConnectionRefusedError :</strong><br>
            → SMTP_SERVER incorrect<br>
            → Port bloqué
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>✅ Tests</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Tester SMTP :</strong><br>
            Lancer script de test (inclus dans docs)<br>
            <code>python api/test_smtp.py</code><br>
            <br>
            <strong>Tester via API :</strong><br>
            Envoyer transaction frauduleuse via POST /predict<br>
            Vérifier email reçu sous 3s<br>
            <br>
            <strong>Logs :</strong><br>
            Inspecter <code>api_metrics.jsonl</code> : champ <code>alert_sent</code>
            </p>
        """), unsafe_allow_html=True)


elif page == "📈 Résultats & KPIs":
    titre("Résultats & KPIs", "Performance modèle et système", "📈")

    # Métriques top-level
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(metric_card("Accuracy", "93.49%", "🎯"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Rappel", "87.10%", "🔍"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("ROC-AUC", "98.20%", "📈"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("F1-Score", "81.47%", "⚖️"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Performance détaillée
    st.markdown("<div class='section-header'>🎯 Performance Modèle (Test Set 20%)</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>📊 Métriques ML</h4>
            <table style='width: 100%; font-size: 1.05rem; color: #1a1a1a;'>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>Accuracy</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700; color: #28a745;'>93.49%</td>
                </tr>
                <tr>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>Précision</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700;'>76.52%</td>
                </tr>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>Rappel (Fraude)</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700; color: #dc3545;'>87.10%</td>
                </tr>
                <tr>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>F1-Score</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700;'>81.47%</td>
                </tr>
                <tr style='background: #f8f9fa;'>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>ROC-AUC</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700; color: #667eea;'>98.20%</td>
                </tr>
                <tr>
                    <td style='padding: 10px; border: 1px solid #ddd;'><strong>Seuil Décision</strong></td>
                    <td style='padding: 10px; border: 1px solid #ddd; font-weight: 700;'>0.304</td>
                </tr>
            </table>
            <p style='margin-top: 15px; color: #1a1a1a; font-size: 0.95rem;'>
            <em>📝 Test set : 9,996 transactions (20% du dataset)</em>
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #0066cc; margin-top: 0;'>🔢 Matrice de Confusion</h4>
            <table style='width: 100%; text-align: center; font-size: 1.1rem; border-collapse: collapse; margin: 15px 0; color: #1a1a1a;'>
                <tr>
                    <td style='padding: 10px; border: 2px solid #ddd; background: #f8f9fa;'></td>
                    <td style='padding: 10px; border: 2px solid #ddd; background: #d4edda; font-weight: 600; color: #1a1a1a;'>Prédit Normal</td>
                    <td style='padding: 10px; border: 2px solid #ddd; background: #f8d7da; font-weight: 600; color: #1a1a1a;'>Prédit Fraude</td>
                </tr>
                <tr>
                    <td style='padding: 10px; border: 2px solid #ddd; background: #d4edda; font-weight: 600; color: #1a1a1a;'>Réel Normal</td>
                    <td style='padding: 15px; border: 2px solid #ddd; background: #d4edda; font-weight: 700; font-size: 1.3rem; color: #1a1a1a;'>
                        7,914<br><span style='font-size: 0.85rem; color: #28a745;'>TN (Vrai Négatif)</span>
                    </td>
                    <td style='padding: 15px; border: 2px solid #ddd; background: #fff3cd; font-weight: 700; font-size: 1.3rem; color: #1a1a1a;'>
                        439<br><span style='font-size: 0.85rem; color: #856404;'>FP (Faux Positif)</span>
                    </td>
                </tr>
                <tr>
                    <td style='padding: 10px; border: 2px solid #ddd; background: #f8d7da; font-weight: 600; color: #1a1a1a;'>Réel Fraude</td>
                    <td style='padding: 15px; border: 2px solid #ddd; background: #f8d7da; font-weight: 700; font-size: 1.3rem; color: #1a1a1a;'>
                        212<br><span style='font-size: 0.85rem; color: #721c24;'>FN (Faux Négatif)</span>
                    </td>
                    <td style='padding: 15px; border: 2px solid #ddd; background: #d4edda; font-weight: 700; font-size: 1.3rem; color: #1a1a1a;'>
                        1,431<br><span style='font-size: 0.85rem; color: #155724;'>TP (Vrai Positif)</span>
                    </td>
                </tr>
            </table>
            <p style='margin-top: 10px; color: #1a1a1a; font-size: 0.95rem;'>
            <strong>Total :</strong> 9,996 transactions | <strong>Taux fraude réel :</strong> 16.43%
            </p>
        """), unsafe_allow_html=True)

    # KPI Système
    st.markdown("<div class='section-header'>⚡ KPIs Système</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>⚡</div>
                <h4 style='color: #667eea;'>Performance API</h4>
                <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
                <strong>Latence moyenne :</strong> ~137ms<br>
                <strong>P95 :</strong> ~180ms<br>
                <strong>Max observé :</strong> ~250ms<br>
                <strong>Throughput :</strong> ~7 req/s
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>📧</div>
                <h4 style='color: #667eea;'>Alertes Email</h4>
                <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
                <strong>Délai envoi :</strong> 2-3s<br>
                <strong>Taux succès :</strong> >99%<br>
                <strong>Format :</strong> HTML<br>
                <strong>Déclencheur :</strong> is_fraud=true
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🐳</div>
                <h4 style='color: #667eea;'>Infrastructure</h4>
                <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
                <strong>Services :</strong> 2 (API + Dashboard)<br>
                <strong>Uptime :</strong> >99.5%<br>
                <strong>Restart policy :</strong> Automatique<br>
                <strong>Healthcheck :</strong> /health 30s
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Interprétation
    st.markdown("<div class='section-header'>🔍 Interprétation & Trade-offs</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>✅ Points Forts</h4>
            <ul class='custom-list' style='color: #1a1a1a;'>
                <li><strong>ROC-AUC 98.2%</strong> : Excellente séparation normales/fraudes</li>
                <li><strong>Rappel 87.1%</strong> : Détecte 87% des fraudes réelles (objectif métier souvent >85%)</li>
                <li><strong>Accuracy 93.5%</strong> : Performances globales élevées</li>
                <li><strong>Faux négatifs limités</strong> : 212/1643 fraudes manquées (12.9%)</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(warning_box("""
            <h4 style='color: #ff6b6b; margin-top: 0;'>⚠️ Améliorations Possibles</h4>
            <ul class='custom-list' style='color: #1a1a1a;'>
                <li><strong>Précision 76.5%</strong> : 439 faux positifs (23.5% d'alertes inutiles)</li>
                <li><strong>Impact UX :</strong> 439 clients légitimes bloqués/contactés à tort</li>
                <li><strong>Tuning seuil :</strong> Augmenter seuil → moins FP mais plus FN</li>
                <li><strong>Features additionnelles :</strong> Géoloc, device fingerprint (si disponible)</li>
            </ul>
        """), unsafe_allow_html=True)

    # Benchmark
    st.markdown("<div class='section-header'>📊 Benchmark Industrie</div>", unsafe_allow_html=True)
    
    df_benchmark = pd.DataFrame({
        'Métrique': ['Accuracy', 'Rappel Fraude', 'ROC-AUC', 'Latence API'],
        'Notre Système': ['93.49%', '87.10%', '98.20%', '~137ms'],
        'Objectif Industrie': ['>90%', '>85%', '>95%', '<200ms'],
        'Status': ['✅ Excellent', '✅ Excellent', '✅ Excellent', '✅ Excellent'],
    })
    
    st.dataframe(df_benchmark, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Conclusion
    st.markdown(success_box("""
        <h3 style='color: #28a745; margin-top: 0;'>🎓 Conclusion du Projet</h3>
        <p style='font-size: 1.15rem; line-height: 1.8;'>
        Ce projet démontre la capacité à concevoir, entraîner, déployer et opérer un <strong>système MLOps complet</strong> 
        de détection de fraude. Les résultats dépassent les benchmarks industriels sur tous les KPIs critiques :
        </p>
        <ul class='custom-list' style='font-size: 1.05rem;'>
            <li><strong>Performance ML :</strong> ROC-AUC 98.2%, Rappel 87.1% (détection fraude efficace)</li>
            <li><strong>Production-ready :</strong> Features stateless, API <200ms, alertes temps réel</li>
            <li><strong>Observabilité :</strong> Dashboard 5 pages, logs JSONL, métriques temps réel</li>
            <li><strong>DevOps :</strong> Docker Compose, healthchecks, restart automatique, volumes persistants</li>
        </ul>
        <p style='font-size: 1.1rem; margin-top: 15px; color: #666;'>
        <strong>🚀 Prêt pour :</strong> Déploiement cloud (AWS/GCP/Azure), scaling horizontal (Kubernetes), 
        monitoring avancé (Prometheus/Grafana), CI/CD (GitHub Actions)
        </p>
    """), unsafe_allow_html=True)

elif page == "🔍 Architecture technique":
    titre("Architecture Technique", "Vue d'ensemble système complet", "🔍")

    # Architecture overview  
    st.markdown("<div class='section-header'>🏗️ Architecture Système</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>📊 DATA LAYER</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>PaySim Dataset :</strong> 49,977 transactions<br>
            <strong>Features CSV :</strong> 27 features engineerées<br>
            <strong>Modèles :</strong> autoencoder.keras, encoder.keras<br>
            <strong>Scaler :</strong> StandardScaler (fit sur train)<br>
            <strong>Seuil :</strong> ae_threshold.npy (0.304)
            </p>
        """), unsafe_allow_html=True)
        
        st.markdown(success_box("""
            <h4 style='color: #28a745; margin-top: 0;'>🚀 API LAYER (FastAPI)</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Port :</strong> 8000<br>
            <strong>Endpoints :</strong> POST /predict, GET /health<br>
            <strong>Process :</strong> 9 inputs → 27 features → Autoencoder → Décision<br>
            <strong>Output :</strong> JSON (is_fraud, error, confidence)<br>
            <strong>Logging :</strong> JSONL metrics<br>
            <strong>Alertes :</strong> SMTP email si fraude
            </p>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #4facfe; margin-top: 0;'>📊 DASHBOARD (Streamlit)</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Port :</strong> 8501<br>
            <strong>Pages :</strong> 5 (Overview, Analytics, Perf, Live, Business)<br>
            <strong>Data source :</strong> api_metrics.jsonl<br>
            <strong>Refresh :</strong> 5s (temps réel)<br>
            <strong>Visualisations :</strong> Plotly, Altair<br>
            <strong>Metrics :</strong> KPI, distributions, tendances
            </p>
        """), unsafe_allow_html=True)
        
        st.markdown(success_box("""
            <h4 style='color: #43e97b; margin-top: 0;'>📧 ALERTES (SMTP)</h4>
            <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
            <strong>Protocol :</strong> SMTP (TLS 587)<br>
            <strong>Trigger :</strong> is_fraud=true<br>
            <strong>Format :</strong> HTML email<br>
            <strong>Latence :</strong> 2-3s<br>
            <strong>Providers :</strong> Gmail, Outlook, SendGrid<br>
            <strong>Config :</strong> .env file
            </p>
        """), unsafe_allow_html=True)
    
    st.markdown(warning_box("""
        <h4 style='color: #ffa500; margin-top: 0;'>🐳 INFRASTRUCTURE (Docker Compose)</h4>
        <p style='font-size: 1.05rem; line-height: 1.8; color: #1a1a1a;'>
        <strong>Orchestration :</strong> Docker Compose<br>
        <strong>Services :</strong> fraud-api (port 8000) + fraud-dashboard (port 8501)<br>
        <strong>Network :</strong> fraud-detection-network (bridge isolé)<br>
        <strong>Volumes :</strong> ./models, ./metrics, ./data (bind mounts persistants)<br>
        <strong>Restart :</strong> unless-stopped (redémarrage automatique)<br>
        <strong>Healthchecks :</strong> GET /health toutes les 30s
        </p>
    """), unsafe_allow_html=True)

    # Stack détaillé
    st.markdown("<div class='section-header'>🛠️ Stack Technologique Détaillée</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🐍 Core ML/Data</h4>
            <ul style='font-size: 1rem; line-height: 1.8; color: #1a1a1a;'>
                <li><strong>Python :</strong> 3.11</li>
                <li><strong>TensorFlow/Keras :</strong> 2.15+</li>
                <li><strong>Scikit-learn :</strong> Preprocessing, metrics</li>
                <li><strong>Pandas :</strong> Data manipulation</li>
                <li><strong>NumPy :</strong> Numerical ops</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🌐 API & Web</h4>
            <ul style='font-size: 1rem; line-height: 1.8; color: #1a1a1a;'>
                <li><strong>FastAPI :</strong> REST API</li>
                <li><strong>Uvicorn :</strong> ASGI server</li>
                <li><strong>Pydantic :</strong> Validation</li>
                <li><strong>Streamlit :</strong> Dashboard</li>
                <li><strong>Plotly/Altair :</strong> Viz</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col3:
        st.markdown(info_box("""
            <h4 style='color: #667eea; margin-top: 0;'>🐳 DevOps/Infra</h4>
            <ul style='font-size: 1rem; line-height: 1.8; color: #1a1a1a;'>
                <li><strong>Docker :</strong> Containerization</li>
                <li><strong>Docker Compose :</strong> Orchestration</li>
                <li><strong>SMTP (smtplib) :</strong> Alerts</li>
                <li><strong>Git :</strong> Version control</li>
            </ul>
        """), unsafe_allow_html=True)

    # Data flow
    st.markdown("<div class='section-header'>🔄 Data Flow Détaillé</div>", unsafe_allow_html=True)
    
    flow = [
        ("1. Ingestion", "Transaction brute (9 champs) arrive via POST /predict", "#667eea"),
        ("2. Validation", "Pydantic vérifie types, valeurs, format", "#764ba2"),
        ("3. Feature Engineering", "Calcul des 27 features (stateless)", "#8e54e9"),
        ("4. Normalisation", "StandardScaler pré-entraîné (fit sur train)", "#f093fb"),
        ("5. Prédiction", "Forward pass dans Autoencoder (27→64→32→16→32→64→27)", "#4facfe"),
        ("6. Reconstruction Error", "MSE entre input et output", "#00f2fe"),
        ("7. Décision", "Comparaison error vs threshold 0.304", "#43e97b"),
        ("8. Logging", "Écriture JSONL avec 15+ métriques", "#38f9d7"),
        ("9. Alerte (si fraude)", "Email SMTP HTML envoyé", "#ffecd2"),
        ("10. Réponse API", "JSON retourné au client (~137ms total)", "#fcb69f"),
    ]
    
    for step, desc, color in flow:
        st.markdown(f"""
            <div style='display: flex; align-items: center; margin: 10px 0;'>
                <div style='background: {color}; color: white; padding: 12px 20px; border-radius: 10px; 
                font-weight: 600; min-width: 200px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    {step}
                </div>
                <div style='flex: 1; margin-left: 20px; font-size: 1.05rem;'>
                    {desc}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scalabilité future
    st.markdown("<div class='section-header'>🚀 Évolutions Futures</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(warning_box("""
            <h4 style='color: #ff6b6b; margin-top: 0;'>📈 Scalabilité</h4>
            <ul class='custom-list' style='color: #1a1a1a;'>
                <li><strong>Kubernetes :</strong> Orchestration cloud-native (HPA)</li>
                <li><strong>Load Balancer :</strong> NGINX/Traefik pour distribution trafic</li>
                <li><strong>Message Queue :</strong> RabbitMQ/Kafka pour découplage</li>
                <li><strong>Cache :</strong> Redis pour features précalculées</li>
            </ul>
        """), unsafe_allow_html=True)
    
    with col2:
        st.markdown(warning_box("""
            <h4 style='color: #ff6b6b; margin-top: 0;'>🔍 Monitoring Avancé</h4>
            <ul class='custom-list' style='color: #1a1a1a;'>
                <li><strong>Prometheus :</strong> Métriques système (CPU, RAM, latence)</li>
                <li><strong>Grafana :</strong> Dashboards avancés + alerting</li>
                <li><strong>ELK Stack :</strong> Logs centralisés (Elasticsearch)</li>
                <li><strong>Model drift :</strong> Surveillance distribution features</li>
            </ul>
        """), unsafe_allow_html=True)
