function get_pensionistas() {
	axios.get('https://jsonplaceholder.typicode.com/todos/1').then(resp => {
		// axios.get('https://4dgxju5lue.execute-api.localhost.localstack.cloud:4566/api/pensionistas').then(resp => {
		var response = {
			"pensionistas": [
				[
					1,
					"João"
				],
				[
					2,
					"Maria"
				],
				[
					3,
					"José"
				],
				[
					4,
					"Marcos"
				],
				[
					5,
					"Antonio"
				]
			]
		}

		// var response = resp.data;
		var table = document.getElementById('table_user').getElementsByTagName('tbody')[0];


		// LIMPAMOS O QUE TINHA ANTES e depois inserimos novos itens
		// isso impede que a tabela reexiba os dados seguidamente
		for (i = table.rows.length - 1; i >= 0; i--) {
			table.deleteRow(i);
		}

		for (var i = 0; i < response.pensionistas.length; i++) {
			// criar uma nova linha de tabela e insere no começo
			var row = table.insertRow(i);

			// cria duas novas células (id, nome)
			//var cell1 = row.insertCell(0);
			//var cell2 = row.insertCell(1);

			for (var j = 0; j < response.pensionistas[i].length; j++)
			{
				// cria uma nova células (id, nome, e etc...)
				var cell1 = row.insertCell(j);
				// altera o texto da célula (id, nome, e etc...)
				cell1.innerHTML = response.pensionistas[i][j];
			}

			// segunda posição da linha i => nome
			//cell2.innerHTML = response.pensionistas[i][0]
			//cell2.innerHTML = response.pensionistas[i][1]

			// print
			console.log(response.pensionistas[i]);
		}
	});
}
