import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd

st.caption("Análise de vínculos e conexões.")
nodes = []
edges = []

with st.expander("Elementos"):
    st.code('''
    A tabela deverá conter na primeira linha os seguintes elementos:
    id: nome, deve ser um campo único para cada elemento.
    label: descrição do elemento ou nome.
    image: link da imagem para o elemento.
    Exemplo:
    id,label,image
    Jean Mortaza, Dev, https://jeanmortaza.com.br/wp-content/uploads/elementor/thumbs/Jean-Mortaza-pmnid0ktr5o6ugp21bbltvnnpbws9w8h72wipsjgug.jpg
    Python, Linguagem, https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png
               ''',language='text')
    arquivo_nodes = st.file_uploader("Carregar CSV com Elementos", type=["csv"])

with st.expander("Adicionar Conexões"):
    st.code('''
    A tabela deverá conter na primeira linha os seguintes elementos:
    source: id do elemento que irá se conectar com o target.
    label: descrição da linha de conexão.
    target: elemento alvo, que será conectado ao source.
    Exemplo:
    source,label,target
    Jean Mortaza, Linguagem, Python
               ''',language='text')
    
    # Criar um dataframe vazio com as colunas source, label e target
    
    option = st.selectbox(
    'Selecionar',
    ('Selecione uma das Opções','Adicionar manualmente', 'Adicionar arquivo CSV'))
    
    if option == 'Adicionar arquivo CSV':
        arquivo_edges = st.file_uploader("Carregar CSV com Conexões", type=["csv"])
        df_up_edges = pd.read_csv(arquivo_edges) #Utilizado para upar a tabela
        
        for index, row_edge in df_up_edges.iterrows():
            edges_source = str(row_edge["source"])
            edges_label = str(row_edge["label"])
            edges_target = str(row_edge["target"])
            edge = Edge(source = edges_source, label = edges_label, target = edges_target )
            edges.append(edge)

    if option == 'Adicionar manualmente':
        df_edges = pd.DataFrame(columns=['source', 'label', 'target'])

        # Criar um formulário para adicionar várias linhas
        with st.form("novo_form"):
            # Criar campos de entrada de texto para cada coluna do dataframe
            source_inputs = st.text_input("Sources (separados por vírgula):")
            label_inputs = st.text_input("Labels (separados por vírgula):")
            target_inputs = st.text_input("Targets (separados por vírgula):")
            submit_button = st.form_submit_button(label="Adicionar linhas")

        # Adicionar as novas linhas ao dataframe quando o usuário clicar no botão
        if submit_button:
            # Dividir os valores inseridos nos campos de entrada de texto em uma lista de strings
            sources = source_inputs.split(",")
            labels = label_inputs.split(",")
            targets = target_inputs.split(",")

            # Criar uma nova linha para cada conjunto de valores
            for i in range(len(sources)):
                new_row = pd.Series({'source': sources[i], 'label': labels[i], 'target': targets[i]})
                df_edges = df_edges.append(new_row, ignore_index=True)

            st.write("Dataframe atualizado:")
            st.dataframe(df_edges)
        
        for index, row_edge in df_edges.iterrows():
            edges_source = str(row_edge["source"])
            edges_label = str(row_edge["label"])
            edges_target = str(row_edge["target"])
            edge = Edge(source = edges_source, label = edges_label, target = edges_target )
            edges.append(edge)

# Adiciona um controle deslizante para definir a distância entre os nós
with st.sidebar:
    st.title("GraPy")
    node_distance = st.slider("Modificar visualização", min_value=50, max_value=500, value=150)
    node_size = st.slider("Tamanho dos nós", min_value=1, max_value=100, value=20)
    select_hierarchical = st.checkbox('Ativar Hierarquia')
    if select_hierarchical:
        node_hierarchical = True
    else:
        node_hierarchical = False
    
    select_central = st.checkbox('Centralizar')
    if select_central:
        node_central = True
    else:
        node_central = False

if arquivo_nodes is not None:
    df_nodes= pd.read_csv(arquivo_nodes)

    for index, row_node in df_nodes.iterrows():
        node_id = str(row_node["id"])
        node_label = str(row_node["id"])
        node_shape= "circularImage"
        node_image= str(row_node["image"])
        node = Node(id=node_id, label=node_label, size=node_size, shape=node_shape,image=node_image)
        nodes.append(node)

    config = Config(width=750, 
                    height=500, 
                    directed=True, 
                    physics=False,
                    style={'center': node_central},
                    node_distance = node_distance, 
                    hierarchical = node_hierarchical)

    agraph(nodes=nodes, edges=edges, config=config)
