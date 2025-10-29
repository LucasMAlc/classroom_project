import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { getMinhasTurmas } from '../services/api';

const DashboardAluno = () => {
  const { user, logout } = useAuth();
  const [turmas, setTurmas] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTurmas();
  }, []);

  const loadTurmas = async () => {
    try {
      const response = await getMinhasTurmas();
      setTurmas(response.data);
    } catch (error) {
      console.error('Erro ao carregar turmas:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Dashboard do Aluno</h1>
        <div style={styles.userInfo}>
          <span>Bem-vindo, {user?.nome}</span>
          <button onClick={logout} style={styles.logoutBtn}>Sair</button>
        </div>
      </div>

      {loading ? (
        <div style={styles.loading}>Carregando turmas...</div>
      ) : (
        <div style={styles.content}>
          <h2>Minhas Turmas ({turmas.length})</h2>
          
          {turmas.length === 0 ? (
            <div style={styles.empty}>Você não está matriculado em nenhuma turma.</div>
          ) : (
            <div style={styles.turmasGrid}>
              {turmas.map((turma) => (
                <div key={turma.id} style={styles.turmaCard}>
                  <div style={styles.turmaHeader}>
                    <h3>{turma.nome}</h3>
                    <span style={{
                      ...styles.badge,
                      backgroundColor: turma.pode_acessar ? '#28a745' : '#ffc107'
                    }}>
                      {turma.pode_acessar ? 'Ativa' : 'Em breve'}
                    </span>
                  </div>
                  
                  <div style={styles.turmaInfo}>
                    <p><strong>Treinamento:</strong> {turma.treinamento.nome}</p>
                    <p><strong>Início:</strong> {new Date(turma.data_inicio).toLocaleDateString()}</p>
                    <p><strong>Conclusão:</strong> {new Date(turma.data_conclusao).toLocaleDateString()}</p>
                    {turma.link_acesso && (
                      <p>
                        <strong>Link:</strong>{' '}
                        <a href={turma.link_acesso} target="_blank" rel="noreferrer" style={styles.link}>
                          Acessar
                        </a>
                      </p>
                    )}
                  </div>

                  <div style={styles.recursos}>
                    <h4>Recursos Disponíveis ({turma.recursos.length})</h4>
                    {turma.recursos.length === 0 ? (
                      <p style={styles.empty}>Nenhum recurso disponível ainda.</p>
                    ) : (
                      <ul style={styles.recursosList}>
                        {turma.recursos.map((recurso) => (
                          <li key={recurso.id} style={styles.recursoItem}>
                            <span style={styles.recursoTipo}>[{recurso.tipo_recurso_display}]</span>
                            <span>{recurso.nome_recurso}</span>
                            {recurso.url_recurso && (
                              <a href={recurso.url_recurso} target="_blank" rel="noreferrer" style={styles.recursoLink}>
                                Abrir
                              </a>
                            )}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
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
  content: {
    backgroundColor: 'white',
    padding: '30px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  loading: {
    textAlign: 'center',
    padding: '40px',
    fontSize: '18px',
    color: '#666',
  },
  empty: {
    textAlign: 'center',
    padding: '20px',
    color: '#999',
  },
  turmasGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))',
    gap: '20px',
    marginTop: '20px',
  },
  turmaCard: {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '20px',
    backgroundColor: '#fafafa',
  },
  turmaHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '15px',
    paddingBottom: '15px',
    borderBottom: '2px solid #e0e0e0',
  },
  badge: {
    padding: '4px 12px',
    borderRadius: '12px',
    fontSize: '12px',
    fontWeight: 'bold',
    color: 'white',
  },
  turmaInfo: {
    marginBottom: '20px',
    lineHeight: '1.8',
  },
  link: {
    color: '#007bff',
    textDecoration: 'none',
  },
  recursos: {
    marginTop: '20px',
    paddingTop: '20px',
    borderTop: '1px solid #ddd',
  },
  recursosList: {
    listStyle: 'none',
    padding: 0,
    margin: '10px 0 0 0',
  },
  recursoItem: {
    padding: '10px',
    marginBottom: '8px',
    backgroundColor: 'white',
    borderRadius: '4px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  recursoTipo: {
    fontWeight: 'bold',
    color: '#007bff',
    fontSize: '12px',
  },
  recursoLink: {
    marginLeft: 'auto',
    color: '#007bff',
    textDecoration: 'none',
    fontSize: '14px',
  },
};

export default DashboardAluno;