import streamlit as st
import pandas as pd
import numpy as np
import scipy.io

st.set_page_config(page_title="Conversor .MAT → .CSV", layout="wide")
st.title("Conversor de arquivo .MAT para .CSV")

# Upload do arquivo .mat
mat_file = st.file_uploader("Selecione o arquivo .mat", type=["mat"])

if mat_file is not None:
    try:
        # Carregar o .mat
        mat = scipy.io.loadmat(mat_file, squeeze_me=True,
                               struct_as_record=False)
        dto = mat.get("dataToExport", None)

        if dto is None:
            st.error("O arquivo não contém a variável 'dataToExport'.")
        else:
            # Bloco 0: COP (Tempo, AP, ML, Fz)
            blk0 = dto[0]
            tempo = np.array(blk0.Tempo).squeeze()
            ap = np.array(blk0.AP).squeeze()
            ml = np.array(blk0.ML).squeeze()
            fz = np.array(blk0.Fz).squeeze()

            df0 = pd.DataFrame({"Tempo": tempo, "AP": ap, "ML": ml, "Fz": fz})

            # Bloco 3: Acelerômetro (accAP, accML, accZ)
            blk3 = dto[3]
            tempo_acc = np.array(blk3.Tempo).squeeze()
            accAP = np.array(blk3.accAP).squeeze()
            accML = np.array(blk3.accML).squeeze()
            accZ = np.array(blk3.accZ).squeeze()

            df3 = pd.DataFrame(
                {"Tempo": tempo_acc, "accAP": accAP, "accML": accML, "accZ": accZ})

            st.success("Arquivo carregado e processado com sucesso!")

            # Mostrar prévia
            st.subheader("Prévia - COP (AP, ML, Fz)")
            st.dataframe(df0.head(20))

            st.subheader("Prévia - Acelerômetro (accAP, accML, accZ)")
            st.dataframe(df3.head(20))

            # Botões para download
            csv0 = df0.to_csv(index=False).encode("utf-8")
            st.download_button("Baixar COP_AP_ML_Fz.csv",
                               csv0, "COP_AP_ML_Fz.csv", "text/csv")

            csv3 = df3.to_csv(index=False).encode("utf-8")
            st.download_button("Baixar ACC_AP_ML_Z.csv", csv3,
                               "ACC_AP_ML_Z.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
