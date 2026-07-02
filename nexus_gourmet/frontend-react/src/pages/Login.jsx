import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../assets/css/login.css';
import logoSite from '../assets/img/logosite2.png';

// NOVOS ÍCONES (Trocado Envelope por User)
const UserIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>);
const LockIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M18 8H17V6C17 3.24 14.76 1 12 1C9.24 1 7 3.24 7 6V8H6C4.9 8 4 8.9 4 10V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V10C20 8.9 19.1 8 18 8ZM9 6C9 4.34 10.34 3 12 3C13.66 3 15 4.34 15 6V8H9V6ZM12 17C10.9 17 10 16.1 10 15C10 13.9 10.9 13 12 13C13.1 13 14 13.9 14 15C14 16.1 13.1 17 12 17Z"/></svg>);
const EyeIcon = () => (<svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17ZM12 9C10.34 9 9 10.34 9 12C9 13.66 10.34 15 12 15C13.66 15 15 13.66 15 12C15 10.34 13.66 9 12 9Z"/></svg>);

export default function Login() {
    const [login, setLogin] = useState('');
    const [senha, setSenha] = useState('');
    const [error, setError] = useState(null);
    const [mostrarSenha, setMostrarSenha] = useState(false);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/login', { cpf: login, senha }, { withCredentials: true });
            if (response.data.success) {
                let cargoUsuario = response.data.data.cargo;
                cargoUsuario = cargoUsuario.toUpperCase().replace('Ç', 'C');
                
                localStorage.setItem('userCargo', cargoUsuario);
                
                if(cargoUsuario === 'ADMINISTRADOR') navigate('/produtos');
                else if(cargoUsuario === 'COZINHEIRO') navigate('/cozinha/fila');
                else navigate('/salao');
            }
        } catch (err) {
            setError(err.response?.data?.message || "Erro ao conectar com o servidor.");
        }
    };

    return (
        <div className="login-page-wrapper">
            <div className="login-card">
                
                {/* Lado Esquerdo - Marca (Escuro) */}
                <div className="login-brand">
                    <div className="brand-overlay"></div>
                    <img src={logoSite} alt="Nexus Gourmet" className="brand-logo" />
                </div>
                
                {/* Lado Direito - Formulário (Claro) */}
                <div className="login-form-container">
                    <div className="login-header">
                        <h1 className="login-title">Olá!</h1>
                        <p className="login-subtitle">Faça login para acessar o sistema</p>
                    </div>
                    
                    <form onSubmit={handleLogin} className="login-form">
                        
                        <div className="input-group">
                            <div className="input-wrapper">
                                {/* Substituído aqui: */}
                                <span className="input-icon"><UserIcon /></span>
                                <input 
                                    type="text" 
                                    placeholder="Digite seu CPF" 
                                    className="input-field" 
                                    value={login} 
                                    onChange={e => setLogin(e.target.value)} 
                                    required 
                                />
                            </div>

                            <div className="input-wrapper">
                                <span className="input-icon"><LockIcon /></span>
                                <input 
                                    type={mostrarSenha ? "text" : "password"} 
                                    placeholder="Sua senha" 
                                    className="input-field" 
                                    value={senha} 
                                    onChange={e => setSenha(e.target.value)} 
                                    required 
                                />
                                <span 
                                    className={`input-action-icon ${mostrarSenha ? 'active' : ''}`} 
                                    onClick={() => setMostrarSenha(!mostrarSenha)}
                                >
                                    <EyeIcon />
                                </span>
                            </div>
                        </div>

                        <div className="login-options">
                            <label className="remember-me">
                                <input type="checkbox" /> 
                                <span>Lembrar de mim</span>
                            </label>
                            <a href="#" className="forgot-password">Esqueceu a senha?</a>
                        </div>
                        
                        {error && <div className="error-message">{error}</div>}

                        <button type="submit" className="login-button">Entrar no Sistema</button>

                    </form>
                </div>
            </div>
        </div>
    );
}