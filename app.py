import re
import streamlit as st

LANGUAGES = {
    "de": {
        "title": "🔍 ID-Online-Checker",
        "description": "Vergleiche zwei ID-Listen, um online verfügbare oder nicht verfügbare IDs zu ermitteln.",
        "mode_label": "Wie möchtest du deine Listen eingeben?",
        "mode_file": "📂 Datei-Upload",
        "mode_manual": "✍️ Manuelle Eingabe",
        "check_mode_label": "Welche IDs möchtest du anzeigen?",
        "check_online": "✅ Online verfügbare IDs",
        "check_offline": "❌ Nicht online verfügbare IDs",
        "file1_label": "Komplette ID-Liste (listmax.txt)",
        "file2_label": "Zu prüfende IDs (check.txt)",
        "manual_list1_label": "**Komplette ID-Liste (listmax)**",
        "manual_list2_label": "**Zu prüfende IDs (check)**",
        "textarea_placeholder": "IDs (eine pro Zeile)",
        "lines_entered": "📝 {count} IDs eingegeben.",
        "clear_button": "🧹 Leeren",
        "results_title": "📊 Ergebnisse",
        "success_result_online": "✅ {found} von {total} IDs sind online verfügbar.",
        "success_result_offline": "❌ {found} von {total} IDs sind nicht online verfügbar.",
        "no_results": "Keine Treffer gefunden.",
        "show_online": "📋 Gefundene IDs anzeigen",
        "download_button": "📥 Ergebnisse herunterladen",
        "incomplete": "Bitte gib für beide Listen entweder eine Datei **oder** Text ein, um fortzufahren.",
        "footer": "🔒 Alle Daten bleiben lokal. Nichts wird gespeichert oder übertragen.",
        "error": "Fehler beim Verarbeiten: {err}",
        "language_label": "Sprache auswählen",
    },
    "en": {
        "title": "🔍 ID Online Checker",
        "description": "Compare two ID lists to find which IDs are available or not available online.",
        "mode_label": "How do you want to enter your lists?",
        "mode_file": "📂 File Upload",
        "mode_manual": "✍️ Manual Input",
        "check_mode_label": "Which IDs do you want to show?",
        "check_online": "✅ IDs available online",
        "check_offline": "❌ IDs NOT available online",
        "file1_label": "Full ID list (listmax.txt)",
        "file2_label": "IDs to check (check.txt)",
        "manual_list1_label": "**Full ID list (listmax)**",
        "manual_list2_label": "**IDs to check (check)**",
        "textarea_placeholder": "One ID per line",
        "lines_entered": "📝 {count} IDs entered.",
        "clear_button": "🧹 Clear",
        "results_title": "📊 Results",
        "success_result_online": "✅ {found} out of {total} IDs are available online.",
        "success_result_offline": "❌ {found} out of {total} IDs are NOT available online.",
        "no_results": "No matches found.",
        "show_online": "📋 Show found IDs",
        "download_button": "📥 Download results",
        "incomplete": "Please enter text or upload files for both lists to proceed.",
        "footer": "🔒 All data is processed locally. Nothing is stored or sent.",
        "error": "Error while processing: {err}",
        "language_label": "Select language",
    }
}

def artikelnummer_bereinigen(zeile):
    zeile = zeile.strip().lower()
    zeile = re.sub(r'^\D+', '', zeile)
    zeile = zeile.lstrip('0')
    return zeile

def get_ids_from_file(file):
    return set(artikelnummer_bereinigen(line.decode("utf-8")) for line in file if line.strip())

def get_ids_from_text(text):
    return set(artikelnummer_bereinigen(line) for line in text.strip().splitlines() if line.strip())

st.set_page_config(page_title="ID Checker", layout="centered", page_icon="🔍")

lang_options = ["de", "en"]
lang_labels = {"de": "🇩🇪 Deutsch", "en": "🇬🇧 English"}
language = st.radio(
    label="🌐",
    options=lang_options,
    index=0,
    format_func=lambda x: lang_labels[x],
    horizontal=True,
    key="lang"
)
t = LANGUAGES[language]

st.title(t["title"])
st.markdown(t["description"])
st.markdown("---")

mode = st.radio(t["mode_label"], [t["mode_file"], t["mode_manual"]], horizontal=True)

if "manual_1" not in st.session_state:
    st.session_state["manual_1"] = ""
if "manual_2" not in st.session_state:
    st.session_state["manual_2"] = ""

def clear_manual_1():
    st.session_state.manual_1 = ""

def clear_manual_2():
    st.session_state.manual_2 = ""

if mode == t["mode_file"]:
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader(t["file1_label"], type=["txt"], key="file1")
    with col2:
        file2 = st.file_uploader(t["file2_label"], type=["txt"], key="file2")
    use_file1 = file1 is not None
    use_file2 = file2 is not None
else:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(t["manual_list1_label"])
        st.text_area(
            t["textarea_placeholder"],
            key="manual_1",
            height=200,
        )
        st.caption(t["lines_entered"].format(count=len(st.session_state.manual_1.strip().splitlines())))
        st.button(t["clear_button"], key="clear1", on_click=clear_manual_1)
    with col2:
        st.markdown(t["manual_list2_label"])
        st.text_area(
            t["textarea_placeholder"],
            key="manual_2",
            height=200,
        )
        st.caption(t["lines_entered"].format(count=len(st.session_state.manual_2.strip().splitlines())))
        st.button(t["clear_button"], key="clear2", on_click=clear_manual_2)

    use_file1 = st.session_state.manual_1.strip() != ""
    use_file2 = st.session_state.manual_2.strip() != ""

check_mode = st.radio(
    t["check_mode_label"],
    [t["check_online"], t["check_offline"]],
    horizontal=True,
    index=0,
    key="check_mode"
)

if use_file1 and use_file2:
    st.markdown("---")
    st.subheader(t["results_title"])
    try:
        ids1 = get_ids_from_file(file1) if mode == t["mode_file"] else get_ids_from_text(st.session_state.manual_1)
        ids2 = get_ids_from_file(file2) if mode == t["mode_file"] else get_ids_from_text(st.session_state.manual_2)

        if check_mode == t["check_online"]:
            result_ids = sorted(ids1.intersection(ids2))
            st.success(t["success_result_online"].format(found=len(result_ids), total=len(ids2)))
        else:
            result_ids = sorted(ids2.difference(ids1))
            st.success(t["success_result_offline"].format(found=len(result_ids), total=len(ids2)))

        with st.expander(t["show_online"]):
            st.code("\n".join(result_ids) if result_ids else t["no_results"])

        filename = "online.txt" if check_mode == t["check_online"] else "nicht_online.txt"

        st.download_button(
            label=t["download_button"],
            data="\n".join(result_ids),
            file_name=filename,
            mime="text/plain"
        )
    except Exception as e:
        st.error(t["error"].format(err=e))
else:
    st.info(t["incomplete"])

st.markdown("---")
st.caption(t["footer"])
