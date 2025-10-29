import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import {
  getTreinamentos,
  createTreinamento,
  deleteTreinamento,
  getTurmas,
  createTurma,
  deleteTurma,
  getRecursos,
  createRecurso,
  deleteRecurso,
} from '../services/api';

const DashboardAdmin = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('treinamentos');
  const [treinamentos, setTreinamentos] = useState([]);
  const [turmas, setTurmas] = useState([]);
  const [recursos, setRecursos] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'treinamentos') {
        const response = await getTreinamentos();
        setTreinamentos(response.data.results || response.data);
      } else if (activeTab === 'turmas') {
        const response = await getTurmas();
        setTurmas(response.data.results || response.data);
      } else if (activeTab === 'recursos') {
        const response = await getRecursos();
        setRecursos(response.data.results || response.data);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTreinamento = async () => {
    const nome = prompt('Nome do treinamento:');
    const descricao = prompt('Descrição:');
    if (nome && descricao) {
      try {
        await createTreinamento({ nome, descricao });
        loadData();
      } catch (error) {
        alert('Erro ao criar treinamento');
      }
    }
  };

  const handleDeleteTreinamento = async (id) => {
    if (window.confirm('Deseja deletar este treinamento?')) {
      try {
        await deleteTreinamento(id);
        loadData();
      } catch (error) {
        alert('Erro ao deletar treinamento');
      }
    }
  };

  const handleCreateTurma = async () => {
    if (treinamentos.length === 0) {
      alert('Crie um treinamento primeiro');
      return;
    }
    const nome = prompt('Nome da turma:');
    const dataInicio = prompt('Data de início (AAAA-MM-DD):');
    const dataConclusao = prompt('Data de conclusão (AAAA-MM-DD):');
    if (nome && dataInicio && dataConclusao) {
      try {
        await createTurma({
          treinamento: treinamentos[0].id,
          nome,
          data_inicio: dataInicio,
          data_conclusao: dataConclusao,
        });
        loadData();
      } catch (error) {
        alert('Erro ao criar turma');
      }
    }
  };

  const handleDeleteTurma = async (id) => {
    if (window.confirm('Deseja deletar esta turma?')) {
      try {
        await deleteTurma(id);
        loadData();
      } catch (error) {
        alert('Erro ao deletar turma');
      }
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Dashboard Admin</h1>
        <div style={styles.userInfo}>
          <span>Bem-vindo, {user?.nome || 'Admin'}</span>
          <button onClick={logout} style={styles.logoutBtn}>Sair</button>
        </div>
      </div>

      <div style={styles.tabs}>
        <button
          style={activeTab === 'treinamentos' ? styles.tabActive : styles.tab}
          onClick={() => setActiveTab('treinamentos')}
        >
          Treinamentos
        </button>
        <button
          style={activeTab === 'turmas' ? styles.tabActive : styles.tab}
          onClick={() => setActiveTab('turmas')}
        >
          Turmas
        </button>
        <button
          style={activeTab === 'recursos' ? styles.tabActive : styles.tab}
          onClick={() => setActiveTab('recursos')}
        >
          Recursos
        </button>
      </div>

      <div style={styles.content}>
        {loading ? (
          <div style={styles.loading}>Carregando...</div>
        ) : (
          <>
            {activeTab === 'treinamentos' && (
              <div>
                <div style={styles.contentHeader}>
                  <h2>Treinamentos ({treinamentos.length})</h2>
                  <button onClick={handleCreateTreinamento} style={styles.createBtn}>
                    Criar Treinamento
                  </button>
                </div>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>ID</th>
                      <th style={styles.th}>Nome</th>
                      <th style={styles.th}>Descrição</th>
                      <th style={styles.th}>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {treinamentos.map((item) => (
                      <tr key={item.id}>
                        <td style={styles.td}>{item.id}</td>
                        <td style={styles.td}>{item.nome}</td>
                        <td style={styles.td}>{item.descricao}</td>
                        <td style={styles.td}>
                          <button
                            onClick={() => handleDeleteTreinamento(item.id)}
                            style={styles.deleteBtn}
                          >
                            Deletar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {activeTab === 'turmas' && (
              <div>
                <div style={styles.contentHeader}>
                  <h2>Turmas ({turmas.length})</h2>
                  <button onClick={handleCreateTurma} style={styles.createBtn}>
                    Criar Turma
                  </button>
                </div>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>ID</th>
                      <th style={styles.th}>Nome</th>
                      <th style={styles.th}>Treinamento</th>
                      <th style={styles.th}>Início</th>
                      <th style={styles.th}>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {turmas.map((item) => (
                      <tr key={item.id}>
                        <td style={styles.td}>{item.id}</td>
                        <td style={styles.td}>{item.nome}</td>
                        <td style={styles.td}>{item.treinamento_nome}</td>
                        <td style={styles.td}>{new Date(item.data_inicio).toLocaleDateString()}</td>
                        <td style={styles.td}>
                          <button
                            onClick={() => handleDeleteTurma(item.id)}
                            style={styles.deleteBtn}
                          >
                            Deletar
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {activeTab === 'recursos' && (
              <div>
                <div style={styles.contentHeader}>
                  <h2>Recursos ({recursos.length})</h2>
                </div>
                <table style={styles.table}>
                  <thead>
                    <tr>
                      <th style={styles.th}>ID</th>
                      <th style={styles.th}>Nome</th>
                      <th style={styles.th}>Tipo</th>
                      <th style={styles.th}>Turma</th>
                      <th style={styles.th}>Draft</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recursos.map((item) => (
                      <tr key={item.id}>
                        <td style={styles.td}>{item.id}</td>
                        <td style={styles.td}>{item.nome_recurso}</td>
                        <td style={styles.td}>{item.tipo_recurso_display}</td>
                        <td style={styles.td}>{item.turma_nome}</td>
                        <td style={styles.td}>{item.draft ? 'Sim' : 'Não'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f5f5f5',
    padding: '20px',
  },
  header: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
  },
  logoutBtn: {
    padding: '8px 16px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  tabs: {
    backgroundColor: 'white',
    padding: '10px',
    borderRadius: '8px',
    marginBottom: '20px',
    display: 'flex',
    gap: '10px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  tab: {
    padding: '10px 20px',
    border: 'none',
    backgroundColor: 'transparent',
    cursor: 'pointer',
    fontSize: '14px',
    borderRadius: '4px',
  },
  tabActive: {
    padding: '10px 20px',
    border: 'none',
    backgroundColor: '#007bff',
    color: 'white',
    cursor: 'pointer',
    fontSize: '14px',
    borderRadius: '4px',
  },
  content: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  contentHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  createBtn: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
  },
  th: {
    backgroundColor: '#f8f9fa',
    padding: '12px',
    textAlign: 'left',
    borderBottom: '2px solid #dee2e6',
  },
  td: {
    padding: '12px',
    borderBottom: '1px solid #dee2e6',
  },
  deleteBtn: {
    padding: '6px 12px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
  },
};

export default DashboardAdmin;