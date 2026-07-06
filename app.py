import streamlit as st

def main():
    st.title("System-Status: Aktiv")
    st.write("Logik-Kern: Geladen.")
    
    # Test-Eingabe
    user_input = st.text_input("Test-Eingabe für Operatoren")
    if user_input:
        st.write(f"Operatoren haben verarbeitet: {user_input}")

if __name__ == "__main__":
    main()
