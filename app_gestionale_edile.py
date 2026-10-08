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

# Custom Styling CSS
st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #2563EB; }
    .metric-card { background-color: #F0F9FF; border-radius: 8px; padding: 15px; border-left: 5px solid #0284C7; }
</style>
""", unsafe_allow_html=True)

# Titolo Principale nell'App
st.title("🏗️ Controllo di Gestione & Sicurezza - Impresa Edile")
st.caption("Sistema integrato configurabile per il calcolo del Costo Orario di Struttura, Break-Even Point, Scadenzario Corsi e Analisi Cantieri")

# ----------------------------------------------------
# BARRA LATERALE DI CONFIGURAZIONE & SQUADRA
# ----------------------------------------------------
st.sidebar.title("🧰 Configurazione & Menu")

st.sidebar.subheader("⚙️ Configurazione Squadra Lavoratori")
num_lavoratori = st.sidebar.number_input(
    "Numero Lavoratori / Operai in Squadra",
    min_value=1,
    max_value=200,
    value=5,
    step=1,
    help="Imposta il numero totale di operai per il calcolo delle ore lavorabili aziendali."
)

ore_annue_procapite = st.sidebar.number_input(
    "Ore Annue Lavorabili per Operaio",
    min_value=100,
    max_value=2500,
    value=1600,
    step=50,
    help="Standard CCNL Edilizia: circa 1600 ore annue effettive per ciascun lavoratore."
)

ore_lavorabili_totali = num_lavoratori * ore_annue_procapite

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Seleziona il Modulo:",
    ["📊 Dashboard & BEP", "📋 Costi Fissi & Normativa", "🦺 Formazione & Sicurezza", "🏗️ Analisi Cantieri", "💰 Prima Nota"]
)

# ----------------------------------------------------
# INIZIALIZZAZIONE SESSION STATE (DATI VARIABILI DA INSERIRE)
# ----------------------------------------------------

if 'costi_fissi' not in st.session_state:
    # Voci di Costo Fisso pronte per l'inserimento degli importi reali da parte dell'utente
    st.session_state.costi_fissi = pd.DataFrame([
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Polizza RCT/RCO (Responsabilità Civile)", "Riferimento_Normativo": "Art. 2087 C.C. / D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Polizza CAR Cantiere (Tutti i Rischi)", "Riferimento_Normativo": "Art. 1669 C.C.", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Assicurazioni & Garanzie", "Voce": "Fideiussioni & Cauzioni Bando/Appalti", "Riferimento_Normativo": "D.Lgs. 36/2023", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Sorveglianza Sanitaria (Medico Competente)", "Riferimento_Normativo": "Art. 41 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Incarico RSPP Esterno / Consulente", "Riferimento_Normativo": "Art. 31 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Budget Formazione Sicurezza Squadra", "Riferimento_Normativo": "Art. 37 D.Lgs. 81/08 & CCNL Edilizia", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Sicurezza & Medicina", "Voce": "Verifica Periodica Attrezzature & Gru", "Riferimento_Normativo": "Art. 71 D.Lgs. 81/08", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Tributi & Cassa Edile", "Voce": "Diritto Annuale CCIAA Catania", "Riferimento_Normativo": "L. 580/1993", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Tributi & Cassa Edile", "Voce": "Iscrizione e Mantenimento Cassa Edile", "Riferimento_Normativo": "D.Lgs. 276/2003 (DURC)", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Consulenze & Software", "Voce": "Commercialista & Bilancio", "Riferimento_Normativo": "D.P.R. 600/73", "Frequenza": "Mensile", "Importo_Annuo": 0.0},
        {"Categoria": "Consulenze & Software", "Voce": "Consulente del Lavoro (Buste Paga)", "Riferimento_Normativo": "L. 12/1979", "Frequenza": "Mensile", "Importo_Annuo": 0.0},
        {"Categoria": "Consulenze & Software", "Voce": "Software Fatturazione SDI & Computo", "Riferimento_Normativo": "D.Lgs. 127/2015", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Mezzi & Sede", "Voce": "Affitto Deposito & Magazzino", "Riferimento_Normativo": "L. 392/1978", "Frequenza": "Mensile", "Importo_Annuo": 0.0},
        {"Categoria": "Mezzi & Sede", "Voce": "Leasing / Noleggio Furgoni", "Riferimento_Normativo": "L. 124/2017", "Frequenza": "Mensile", "Importo_Annuo": 0.0},
        {"Categoria": "Mezzi & Sede", "Voce": "RCA & Assicurazione Mezzi Aziendali", "Riferimento_Normativo": "Art. 193 Codice della Strada", "Frequenza": "Annuale", "Importo_Annuo": 0.0},
        {"Categoria": "Struttura & Compensi", "Voce": "Compenso Amministratore / Titolare", "Riferimento_Normativo": "Art. 2389 C.C.", "Frequenza": "Mensile", "Importo_Annuo": 0.0},
        {"Categoria": "Struttura & Compensi", "Voce": "Premio Annuale INAIL (Autoliquidazione)", "Riferimento_Normativo": "D.P.R. 1124/1965", "Frequenza": "Annuale", "Importo_Annuo": 0.0}
    ])

if 'dipendenti' not in st.session_state:
    st.session_state.dipendenti = pd.DataFrame(columns=[
        "ID", "Nome", "Ruolo", "Regime_Cassa", "Scadenza_RSPP", "Stato_RSPP"
    ])

if 'cantieri' not in st.session_state:
    st.session_state.cantieri = pd.DataFrame(columns=[
        "Codice", "Cliente", "Ricavo_Pattuito", "Costi_Variabili_Diretti", "Ore_Lavorate"
    ])

if 'prima_nota' not in st.session_state:
    st.session_state.prima_nota = pd.DataFrame(columns=[
        "Data", "Descrizione", "Tipo", "Importo", "IVA"
    ])

# Calcoli generali di supporto
totale_costi_fissi = st.session_state.costi_fissi["Importo_Annuo"].sum()
costo_orario_struttura = totale_costi_fissi / ore_lavorabili_totali if ore_lavorabili_totali > 0 else 0

# ----------------------------------------------------
# MODULO 1: DASHBOARD & BREAK-EVEN POINT
# ----------------------------------------------------
if pagina == "📊 Dashboard & BEP":
    st.header("📊 Dashboard Economica & Break-Even Point (BEP)")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Totale Costi Fissi Annui", f"€ {totale_costi_fissi:,.2f}")
    col2.metric(f"Ore Squadra ({num_lavoratori} op.)", f"{ore_lavorabili_totali:,.0f} h")
    col3.metric("Costo Orario di Struttura", f"€ {costo_orario_struttura:,.2f} / ora")
    
    # Input interattivo Margine di Contribuzione Medio %
    mdc_pct = st.slider("Margine di Contribuzione Medio Stimato (%)", min_value=10.0, max_value=60.0, value=35.0, step=1.0)
    
    bep_fatturato = totale_costi_fissi / (mdc_pct / 100.0) if mdc_pct > 0 else 0
    col4.metric("Fatturato Minimo BEP", f"€ {bep_fatturato:,.2f}")
    
    st.markdown("---")
    
    st.subheader("💡 Analisi del Punto di Pareggio (Break-Even Point)")
    if totale_costi_fissi == 0:
        st.warning("⚠️ **Attenzione**: Inserisci i dati dei Costi Fissi nel modulo **📋 Costi Fissi & Normativa** per calcolare il Costo Orario di Struttura e il BEP reale.")
    else:
        st.info(f"""
        * **Costo Orario di Struttura per Operaio**: Per ogni ora lavorata da ciascuno dei **{num_lavoratori} operai** nei cantieri (su un totale di **{ore_lavorabili_totali:,} ore/anno**), occorre imputare **€ {costo_orario_struttura:.2f}** per coprire i costi fissi aziendali.
        * **Fatturato Minimo Annuo**: Con un margine di contribuzione medio del **{mdc_pct}%**, la tua impresa deve fatturare almeno **€ {bep_fatturato:,.2f}** all'anno prima di iniziare a generare un utile netto reale.
        """)
    
    # Grafico Ripartizione Costi Fissi per Categoria
    df_cat = st.session_state.costi_fissi.groupby("Categoria")["Importo_Annuo"].sum().reset_index()
    if df_cat["Importo_Annuo"].sum() > 0:
        fig = px.pie(df_cat, values='Importo_Annuo', names='Categoria', title='Ripartizione Costi Fissi Aziendali', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("ℹ️ Nessun costo fisso ancora valorizzato. Inserisci gli importi nel modulo dei Costi Fissi per generare il grafico.")

# ----------------------------------------------------
# MODULO 2: COSTI FISSI & NORMATIVA
# ----------------------------------------------------
elif pagina == "📋 Costi Fissi & Normativa":
    st.header("📋 Costi Fissi di Struttura & Riferimenti Legislativi")
    st.caption("Inserisci o modifica i dati degli importi annui per le varie voci di spesa fissa correlate alle norme italiane vigenti.")
    
    # Editor dati interattivo
    df_costi_edited = st.data_editor(
        st.session_state.costi_fissi,
        num_rows="dynamic",
        column_config={
            "Importo_Annuo": st.column_config.NumberColumn("Importo Annuo (€)", format="€ %.2f", min_value=0.0),
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
        "Corso / Abilitazione": ["Formazione Ingresso Rischio Alto (16h)", "Preposto alla Sicurezza (8-12h)", "Lavori in Quota & DPI 3ª Cat. (8h)", "Montaggio Ponteggi PiMUS (28h)", "Primo Soccorso Gruppo A (16h)", "Antincendio Livello 2 (8h)", "Patentino PLE / Gru (10-12h)", "RSPP Datore di Lavoro (48h)"],
        "Normativa": ["D.Lgs. 81/08 Art. 37 & CCNL", "D.Lgs. 81/08 Art. 37 & L. 215/21", "D.Lgs. 81/08 Art. 77 / 115", "D.Lgs. 81/08 Art. 136 All. XXI", "D.Lgs. 81/08 Art. 45 / DM 388", "D.Lgs. 81/08 Art. 46 / DM 2021", "D.Lgs. 81/08 Art. 73 Accordo 2012", "D.Lgs. 81/08 Art. 34"],
        "Cassa Edile ESEC Catania": ["Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Finanziato", "Gratuito / Agevolato", "Mercato Privato"],
        "Mercato Privato Catania": ["€ 120 - € 160", "€ 120 - € 180", "€ 150 - € 180", "€ 280 - € 380", "€ 180 - € 240", "€ 150 - € 220", "€ 150 - € 220", "€ 350 - € 500"]
    }
    st.table(pd.DataFrame(tariffe_data))
    
    st.markdown("---")
    st.subheader("Registro Dipendenti & Scadenze Attestati")
    st.caption("Aggiungi o gestisci i lavoratori del tuo organico inserendo i dati reali.")
    
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

    st.markdown("---")
    st.subheader("➕ Aggiungi Nuovo Dipendente / Lavoratore")
    with st.form("form_nuovo_dipendente"):
        col_d1, col_d2 = st.columns(2)
        nome_dip = col_d1.text_input("Nome e Cognome", "")
        ruolo_dip = col_d2.text_input("Ruolo / Mansione", "Muratore Qualificato")
        regime_dip = col_d1.selectbox("Regime Cassa Edile", ["Iscritto Cassa Edile ESEC", "Mercato Privato Catania"])
        scad_dip = col_d2.date_input("Scadenza Formazione", datetime.now() + timedelta(days=365))
        stato_dip = col_d1.selectbox("Stato Formazione", ["VALIDO", "IN SCADENZA", "SCADUTO"])
        
        btn_dip = st.form_submit_button("Aggiungi Dipendente")
        if btn_dip:
            if nome_dip.strip() != "":
                nuovo_id = len(st.session_state.dipendenti) + 1
                row_dip = pd.DataFrame([{"ID": nuovo_id, "Nome": nome_dip, "Ruolo": ruolo_dip, "Regime_Cassa": regime_dip, "Scadenza_RSPP": str(scad_dip), "Stato_RSPP": stato_dip}])
                st.session_state.dipendenti = pd.concat([st.session_state.dipendenti, row_dip], ignore_index=True)
                st.success(f"Dipendente {nome_dip} aggiunto al registro!")
                st.rerun()
            else:
                st.error("Inserisci il nome e cognome del dipendente.")

# ----------------------------------------------------
# MODULO 4: ANALISI CANTIERI
# ----------------------------------------------------
elif pagina == "🏗️ Analisi Cantieri":
    st.header("🏗️ Analisi Economica per Cantiere di Ristrutturazione")
    st.caption("Calcolo del Margine di Contribuzione e Imputazione della Quota Fissa Oraria di Struttura.")
    
    if len(st.session_state.cantieri) > 0:
        df_cantieri = st.session_state.cantieri.copy()
        
        # Calcolo Campi Derivati
        df_cantieri["Ricavo_Pattuito"] = pd.to_numeric(df_cantieri["Ricavo_Pattuito"], errors='coerce').fillna(0.0)
        df_cantieri["Costi_Variabili_Diretti"] = pd.to_numeric(df_cantieri["Costi_Variabili_Diretti"], errors='coerce').fillna(0.0)
        df_cantieri["Ore_Lavorate"] = pd.to_numeric(df_cantieri["Ore_Lavorate"], errors='coerce').fillna(0)

        df_cantieri["Margine_Contribuzione_€"] = df_cantieri["Ricavo_Pattuito"] - df_cantieri["Costi_Variabili_Diretti"]
        df_cantieri["Margine_Contribuzione_%"] = np.where(df_cantieri["Ricavo_Pattuito"] > 0, (df_cantieri["Margine_Contribuzione_€"] / df_cantieri["Ricavo_Pattuito"]) * 100, 0.0)
        df_cantieri["Quota_Costi_Fissi_Imputata"] = df_cantieri["Ore_Lavorate"] * costo_orario_struttura
        df_cantieri["Margine_Netto_Cantiere_€"] = df_cantieri["Margine_Contribuzione_€"] - df_cantieri["Quota_Costi_Fissi_Imputata"]
        df_cantieri["Margine_Netto_%"] = np.where(df_cantieri["Ricavo_Pattuito"] > 0, (df_cantieri["Margine_Netto_Cantiere_€"] / df_cantieri["Ricavo_Pattuito"]) * 100, 0.0)
        
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
    else:
        st.info("ℹ️ Nessun cantiere ancora registrato. Utilizza il modulo qui sotto per inserire i dati dei tuoi cantieri.")

    st.markdown("---")
    st.subheader("➕ Aggiungi un Nuovo Cantiere")
    with st.form("form_nuovo_cantiere"):
        col_a, col_b = st.columns(2)
        cod = col_a.text_input("Codice Cantiere", "CNT-2026-01")
        cli = col_b.text_input("Cliente / Descrizione Cantiere", "")
        ric = col_a.number_input("Ricavo Pattuito (€)", min_value=0.0, value=50000.0)
        c_var = col_b.number_input("Costi Variabili Diretti (€)", min_value=0.0, value=25000.0)
        ore = col_a.number_input("Ore Previste / Lavorate", min_value=0, value=500)
        
        btn_submit = st.form_submit_button("Salva Cantiere")
        if btn_submit:
            if cli.strip() != "":
                nuovo_row = pd.DataFrame([{"Codice": cod, "Cliente": cli, "Ricavo_Pattuito": ric, "Costi_Variabili_Diretti": c_var, "Ore_Lavorate": ore}])
                st.session_state.cantieri = pd.concat([st.session_state.cantieri, nuovo_row], ignore_index=True)
                st.success(f"Cantiere {cod} aggiunto con successo!")
                st.rerun()
            else:
                st.error("Inserisci una descrizione o il nome del cliente per il cantiere.")

# ----------------------------------------------------
# MODULO 5: PRIMA NOTA
# ----------------------------------------------------
elif pagina == "💰 Prima Nota":
    st.header("💰 Registro Prima Nota - Entrate & Uscite")
    
    if len(st.session_state.prima_nota) > 0:
        df_pn = st.session_state.prima_nota.copy()
        st.dataframe(df_pn, use_container_width=True)
    else:
        st.info("ℹ️ Nessun movimento di prima nota registrato. Compila il form qui sotto per registrare la prima operazione.")

    st.markdown("---")
    st.subheader("➕ Registra Movimento di Cassa / Banca")
    with st.form("form_prima_nota"):
        c1, c2 = st.columns(2)
        d_m = c1.date_input("Data Movimento", datetime.now())
        desc = c2.text_input("Descrizione / Causale Movimento", "")
        tipo = c1.selectbox("Tipo Movimento", ["Entrata Cantiere", "Costo Variabile Cantiere", "Costo Fisso Struttura"])
        imp = c2.number_input("Importo Imponibile (€)", min_value=0.0, value=1000.0)
        iva = c1.number_input("IVA (€)", min_value=0.0, value=220.0)
        
        btn_pn = st.form_submit_button("Registra Movimento")
        if btn_pn:
            if desc.strip() != "":
                n_row = pd.DataFrame([{"Data": str(d_m), "Descrizione": desc, "Tipo": tipo, "Importo": imp, "IVA": iva}])
                st.session_state.prima_nota = pd.concat([st.session_state.prima_nota, n_row], ignore_index=True)
                st.success("Movimento di prima nota registrato correttamente!")
                st.rerun()
            else:
                st.error("Inserisci la descrizione o la causale del movimento.")
