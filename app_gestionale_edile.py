import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Configurazione Iniziale Pagina Streamlit
st.set_page_config(
    page_title="Gestionale Impresa Edile & Sicurezza",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titolo Principale nell'App
st.title("🏗️ Controllo di Gestione & Sicurezza - Impresa Edile")
st.caption("Sistema integrato per il calcolo del Costo Orario di Struttura, Break-Even Point, Scadenzario Corsi (Catania) e Analisi Cantieri")

# ----------------------------------------------------
# INIZIALIZZAZIONE SESSION STATE (DATABASE IN MEMORIA)
# ----------------------------------------------------

if 'costi_fissi' not in st.session_state:
    st.session_state.costi_fissi = pd.DataFrame([
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Polizza RCT/RCO (Responsabilità Civile)", "Riferimento_Normativo": "Art. 2087 C.C. / D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 2800.0},
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Polizza CAR Cantiere (Tutti i Rischi)", "Riferimento_Normativo": "Art. 1669 C.C.", "Frequenza": "Annuale", "Importo_Annuo": 1800.0},
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Fideiussioni & Cauzioni Bando/Appalti", "Riferimento_Normativo": "D.Lgs. 36/2023", "Frequenza": "Annuale", "Importo_Annuo": 1200.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Sorveglianza Sanitaria (Medico Competente)", "Riferimento_Normativo": "Art. 41 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 1440.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Incarico RSPP Esterno / Consulente", "Riferimento_Normativo": "Art. 31 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 1800.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Budget Formazione Sicurezza Squadra", "Riferimento_Normativo": "Art. 37 D.Lgs. 81/08 & CCNL Edilizia", "Frequenza": "Annuale", "Importo_Annuo": 1500.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Verifica Periodica Attrezzature & Gru", "Riferimento_Normativo": "Art. 71 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 850.0},
        {"Categoria": "Tributi & Cassa Edile", "Voce": "Diritto Annuale CCIAA Catania", "Riferimento_Normativo": "L. 580/1993", "Frequenza": "Annuale", "Importo_Annuo": 200.0},
        {"Categoria": "Tributi & Cassa Edile", "Voce": "Iscrizione e Mantenimento Cassa Edile", "Riferimento_Normativo": "D.Lgs. 276/2003 (DURC)", "Frequenza": "Annuale", "Importo_Annuo": 600.0},
        {"Categoria": "Consulenze & Software", "Voce": "Commercialista & Bilancio", "Riferimento_Normativo": "D.P.R. 600/73", "Frequenza": "Mensile", "Importo_Annuo": 3600.0},
        {"Categoria": "Consulenze & Software", "Voce": "Consulente del Lavoro (Buste Paga)", "Riferimento_Normativo": "L. 12/1979", "Frequenza": "Mensile", "Importo_Annuo": 3840.0},
        {"Categoria": "Consulenze & Software", "Voce": "Software Fatturazione SDI & Computo", "Riferimento_Normativo": "D.Lgs. 127/2015", "Frequenza": "Annuale", "Importo_Annuo": 750.0},
        {"Categoria": "Mezzi & Sede", "Voce": "Affitto Deposito & Magazzino", "Riferimento_Normativo": "L. 392/1978", "Frequenza": "Mensile", "Importo_Annuo": 9600.0},
        {"Categoria": "Mezzi & Sede", "Voce": "Leasing / Noleggio Furgoni", "Riferimento_Normativo": "L. 124/2017", "Frequenza": "Mensile", "Importo_Annuo": 10800.0},
        {"Categoria": "Mezzi & Sede", "Voce": "RCA & Assicurazione Mezzi Aziendali", "Riferimento_Normativo": "Art. 193 Codice della Strada", "Frequenza": "Annuale", "Importo_Annuo": 3200.0},
        {"Categoria": "Struttura & Compensi", "Voce": "Compenso Amministratore / Titolare", "Riferimento_Normativo": "Art. 2389 C.C.", "Frequenza": "Mensile", "Importo_Annuo": 30000.0},
        {"Categoria": "Struttura & Compensi", "Voce": "Premio Annuale INAIL (Autoliquidazione)", "Riferimento_Normativo": "D.P.R. 1124/1965", "Frequenza": "Annuale", "Importo_Annuo": 4200.0}
    ])

if 'dipendenti' not in st.session_state:
    st.session_state.dipendenti = pd.DataFrame([
        {"ID": 1, "Nome": "Mario Rossi (Datore di Lavoro)", "Ruolo": "Datore di Lavoro / RSPP", "Regime_Cassa": "Mercato Privato Catania", "Scadenza_RSPP": "2027-05-15", "Stato_RSPP": "VALIDO"},
        {"ID": 2, "Nome": "Giuseppe Verdi", "Ruolo": "Capocantiere / Preposto", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2026-11-20", "Stato_RSPP": "IN SCADENZA"},
        {"ID": 3, "Nome": "Giuseppe Russo", "Ruolo": "Muratore Specializzato / Ponteggiatore", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2028-02-10", "Stato_RSPP": "VALIDO"},
        {"ID": 4, "Nome": "Antonio Esposito", "Ruolo": "Gruista / Operatore PLE", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2026-10-15", "Stato_RSPP": "IN SCADENZA"},
        {"ID": 5, "Nome": "Salvatore Catania", "Ruolo": "Muratore Qualificato", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2027-09-01", "Stato_RSPP": "VALIDO"},
        {"ID": 6, "Nome": "Francesco Bella", "Ruolo": "Cartongessista / Tinteggiatore", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2027-12-10", "Stato_RSPP": "VALIDO"},
        {"ID": 7, "Nome": "Angelo Messina", "Ruolo": "Idraulico / Impiantista", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2025-08-30", "Stato_RSPP": "SCADUTO"},
        {"ID": 8, "Nome": "Davide Siracusa", "Ruolo": "Elettricista di Cantiere", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2027-04-18", "Stato_RSPP": "VALIDO"},
        {"ID": 9, "Nome": "Carmelo Licata", "Ruolo": "Apprendista Edile", "Regime_Cassa": "Iscritto Cassa Edile ESEC", "Scadenza_RSPP": "2028-01-15", "Stato_RSPP": "VALIDO"}
    ])

if 'cantieri' not in st.session_state:
    st.session_state.cantieri = pd.DataFrame([
        {"Codice": "CNT-2026-01", "Cliente": "Condominio Corso Italia - Catania", "Ricavo_Pattuito": 125000.0, "Costi_Variabili_Diretti": 68000.0, "Ore_Lavorate": 1450},
        {"Codice": "CNT-2026-02", "Cliente": "Ristrutturazione Villa Acireale", "Ricavo_Pattuito": 85000.0, "Costi_Variabili_Diretti": 42000.0, "Ore_Lavorate": 980},
        {"Codice": "CNT-2026-03", "Cliente": "Restauro Appartamento Via Etnea", "Ricavo_Pattuito": 45000.0, "Costi_Variabili_Diretti": 21000.0, "Ore_Lavorate": 520}
    ])

if 'prima_nota' not in st.session_state:
    st.session_state.prima_nota = pd.DataFrame([
        {"Data": "2026-01-10", "Descrizione": "Acconto Cantiere Corso Italia", "Tipo": "Entrata Cantiere", "Importo": 35000.0, "IVA": 3500.0},
        {"Data": "2026-01-15", "Descrizione": "Acquisto Materiali Edili Cementi/Tavole", "Tipo": "Costo Variabile Cantiere", "Importo": 12400.0, "IVA": 2728.0},
        {"Data": "2026-01-31", "Descrizione": "Affitto Deposito Catania Gennaio", "Tipo": "Costo Fisso Struttura", "Importo": 800.0, "IVA": 176.0},
        {"Data": "2026-02-05", "Descrizione": "Canone Leasing Furgoni Febbraio", "Tipo": "Costo Fisso Struttura", "Importo": 900.0, "IVA": 198.0}
    ])

# ----------------------------------------------------
# BARRA LATERALE DI NAVIGAZIONE
# ----------------------------------------------------
st.sidebar.title("🧰 Menu Gestionale")
pagina = st.sidebar.radio(
    "Seleziona il Modulo:",
    ["📊 Dashboard & BEP", "📋 Costi Fissi & Normativa", "🦺 Formazione & Sicurezza", "🏗️ Analisi Cantieri", "💰 Prima Nota"]
)

totale_costi_fissi = st.session_state.costi_fissi["Importo_Annuo"].sum()
ore_lavorabili_totali = 8 * 1600
costo_orario_struttura = totale_costi_fissi / ore_lavorabili_totali if ore_lavorabili_totali > 0 else 0

# ----------------------------------------------------
# MODULO 1: DASHBOARD & BREAK-EVEN POINT
# ----------------------------------------------------
if pagina == "📊 Dashboard & BEP":
    st.header("📊 Dashboard Economica & Break-Even Point (BEP)")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totale Costi Fissi Annui", f"€ {totale_costi_fissi:,.2f}")
    col2.metric("Ore Lavorabili Squadra (8 op.)", f"{ore_lavorabili_totali:,.0f} h")
    col3.metric("Costo Orario di Struttura", f"€ {costo_orario_struttura:,.2f} / ora")
    
    mdc_pct = st.slider("Margine di Contribuzione Medio Stimato (%)", min_value=10.0, max_value=60.0, value=35.0, step=1.0)
    bep_fatturato = totale_costi_fissi / (mdc_pct / 100.0)
    col4.metric("Fatturato Minimo BEP", f"€ {bep_fatturato:,.2f}")
    
    st.markdown("---")
    st.subheader("💡 Analisi del Punto di Pareggio (Break-Even Point)")
    st.info(f"""
    * **Costo Orario di Struttura per Operaio**: Per ogni ora lavorata da ciascuno degli 8 operai nei cantieri, occorre imputare **€ {costo_orario_struttura:.2f}** per coprire i costi fissi aziendali.
    * **Fatturato Minimo Annuo**: Con un margine di contribuzione medio del **{mdc_pct}%**, la tua impresa deve fatturare almeno **€ {bep_fatturato:,.2f}** all'anno prima di iniziare a generare un utile netto reale.
    """)
    
    df_cat = st.session_state.costi_fissi.groupby("Categoria")["Importo_Annuo"].sum().reset_index()
    fig = px.pie(df_cat, values='Importo_Annuo', names='Categoria', title='Ripartizione Costi Fissi Aziendali', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# MODULO 2: COSTI FISSI & NORMATIVA
# ----------------------------------------------------
elif pagina == "📋 Costi Fissi & Normativa":
    st.header("📋 Costi Fissi di Struttura & Riferimenti Legislativi")
    st.caption("Elenco completo delle voci di spesa fissa correlate alle norme italiane vigenti.")
    
    df_costi_edited = st.data_editor(
        st.session_state.costi_fissi,
        num_rows="dynamic",
        column_config={
            "Importo_Annuo": st.column_config.NumberColumn("Importo Annuo (€)", format="€ %.2f"),
            "Frequenza": st.column_config.SelectboxColumn("Frequenza", options=["Annuale", "Mensile", "Trimestrale"])
        },
        use_container_width=True
    )
    st.session_state.costi_fissi = df_costi_edited
    st.success(f"Totale Costi Fissi Aggiornato: **€ {st.session_state.costi_fissi['Importo_Annuo'].sum():,.2f}**")

# ----------------------------------------------------
# MODULO 3: FORMAZIONE & SICUREZZA (CATANIA)
# ----------------------------------------------------
elif pagina == "🦺 Formazione & Sicurezza":
    st.header("🦺 Registro Formazione Sicurezza - Impresa & Dipendenti")
    st.caption("Scadenzario corsi e gestione tariffe (Cassa Edile ESEC Catania vs Mercato Privato)")
    
    st.subheader("Listino Tariffe di Riferimento - Catania")
    tariffe_data = {
        "Corso / Abilitazione": ["Formazione Ingresso Rischio Alto (16h)", "Preposto alla Sicurezza (8-12h)", "Lavori in Quota & DPI 3a Cat. (8h)", "Montaggio Ponteggi PiMUS (28h)", "Primo Soccorso Gruppo A (16h)", "Antincendio Livello 2 (8h)", "Patentino PLE / Gru (10-12h)", "RSPP Datore di Lavoro (48h)"],
        "Normativa": ["D.Lgs. 81/08 Art. 37 & CCNL", "D.Lgs. 81/08 Art. 37 & L. 215/21", "D.Lgs. 81/08 Art. 77 / 115", "D.Lgs. 81/08 Art. 136 All. XXI", "D.Lgs. 81/08 Art. 45 / DM 388", "D.Lgs. 81/08 Art. 46 / DM 2021", "D.Lgs. 81/08 Art. 73 Accordo 2012", "D.Lgs. 81/08 Art. 34"],
        "Cassa Edile ESEC Catania": ["Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Agevolato", "Mercato Privato"],
        "Mercato Privato Catania": ["€ 120 - € 160", "€ 120 - € 180", "€ 150 - € 180", "€ 280 - € 380", "€ 180 - € 240", "€ 150 - € 220", "€ 150 - € 220", "€ 350 - € 500"]
    }
    st.table(pd.DataFrame(tariffe_data))
    
    st.markdown("---")
    st.subheader("Registro Dipendenti & Scadenze Attestati")
    
    df_dip_edited = st.data_editor(
        st.session_state.dipendenti,
        num_rows="dynamic",
        column_config={
            "Regime_Cassa": st.column_config.SelectboxColumn("Regime Tariffario", options=["Iscritto Cassa Edile ESEC", "Mercato Privato Catania"]),
            "Stato_RSPP": st.column_config.SelectboxColumn("Stato Formazione", options=["VALIDO", "IN SCADENZA", "SCADUTO"])
        },
        use_container_width=True
    )
    st.session_state.dipendenti = df_dip_edited

# ----------------------------------------------------
# MODULO 4: ANALISI CANTIERI
# ----------------------------------------------------
elif pagina == "🏗️ Analisi Cantieri":
    st.header("🏗️ Analisi Economica per Cantiere di Ristrutturazione")
    st.caption("Calcolo del Margine di Contribuzione e Imputazione della Quota Fissa Oraria di Struttura.")
    
    df_cantieri = st.session_state.cantieri.copy()
    
    df_cantieri["Margine_Contribuzione_€"] = df_cantieri["Ricavo_Pattuito"] - df_cantieri["Costi_Variabili_Diretti"]
    df_cantieri["Margine_Contribuzione_%"] = (df_cantieri["Margine_Contribuzione_€"] / df_cantieri["Ricavo_Pattuito"]) * 100
    df_cantieri["Quota_Costi_Fissi_Imputata"] = df_cantieri["Ore_Lavorate"] * costo_orario_struttura
    df_cantieri["Margine_Netto_Cantiere_€"] = df_cantieri["Margine_Contribuzione_€"] - df_cantieri["Quota_Costi_Fissi_Imputata"]
    df_cantieri["Margine_Netto_%"] = (df_cantieri["Margine_Netto_Cantiere_€"] / df_cantieri["Ricavo_Pattuito"]) * 100
    
    st.dataframe(
        df_cantieri.style.format({
            "Ricavo_Pattuito": "€ {:,.2f}",
            "Costi_Variabili_Diretti": "€ {:,.2f}",
            "Margine_Contribuzione_€": "€ {:,.2f}",
            "Margine_Contribuzione_%": "{:.1f} %",
            "Quota_Costi_Fissi_Imputata": "€ {:,.2f}",
            "Margine_Netto_Cantiere_€": "€ {:,.2f}",
            "Margine_Netto_%": "{:.1f} %"
        }),
        use_container_width=True
    )
    
    st.markdown("---")
    st.subheader("➕ Aggiungi un Nuovo Cantiere")
    with st.form("form_nuovo_cantiere"):
        col_a, col_b = st.columns(2)
        cod = col_a.text_input("Codice Cantiere", "CNT-2026-04")
        cli = col_b.text_input("Cliente / Descrizione", "Ristrutturazione Appartamento Corso Sicilia")
        ric = col_a.number_input("Ricavo Pattuito (€)", min_value=0.0, value=60000.0)
        c_var = col_b.number_input("Costi Variabili Diretti (€)", min_value=0.0, value=32000.0)
        ore = col_a.number_input("Ore Previste / Lavorate", min_value=0, value=700)
        
        btn_submit = st.form_submit_button("Salva Cantiere")
        if btn_submit:
            nuovo_row = pd.DataFrame([{"Codice": cod, "Cliente": cli, "Ricavo_Pattuito": ric, "Costi_Variabili_Diretti": c_var, "Ore_Lavorate": ore}])
            st.session_state.cantieri = pd.concat([st.session_state.cantieri, nuovo_row], ignore_index=True)
            st.success(f"Cantiere {cod} aggiunto con successo!")
            st.rerun()

# ----------------------------------------------------
# MODULO 5: PRIMA NOTA
# ----------------------------------------------------
elif pagina == "💰 Prima Nota":
    st.header("💰 Registro Prima Nota - Entrate & Uscite")
    
    df_pn = st.session_state.prima_nota.copy()
    st.dataframe(df_pn, use_container_width=True)
    
    st.subheader("➕ Registra Movimento di Cassa")
    with st.form("form_prima_nota"):
        c1, c2 = st.columns(2)
        d_m = c1.date_input("Data Movimento", datetime.now())
        desc = c2.text_input("Descrizione / Causale", "Incasso Saldo Cantiere")
        tipo = c1.selectbox("Tipo Movimento", ["Entrata Cantiere", "Costo Variabile Cantiere", "Costo Fisso Struttura"])
        imp = c2.number_input("Importo (€)", min_value=0.0, value=5000.0)
        iva = c1.number_input("IVA (€)", min_value=0.0, value=1100.0)
        
        btn_pn = st.form_submit_button("Registra Movimento")
        if btn_pn:
            n_row = pd.DataFrame([{"Data": str(d_m), "Descrizione": desc, "Tipo": tipo, "Importo": imp, "IVA": iva}])
            st.session_state.prima_nota = pd.concat([st.session_state.prima_nota, n_row], ignore_index=True)
            st.success("Movimento registrato correttamente!")
            st.rerun()
