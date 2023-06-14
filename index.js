function get_order() {
	// axios.get('https://jsonplaceholder.typicode.com/todos/1').then(resp => {
	// axios.get('https://w0q1zo1lwf.execute-api.localhost.localstack.cloud:4566/api/order').then(resp => {
	axios.get('http://localhost:4566/restapis/lbxs8haiad/local/_user_request_/order').then(resp => {
		// var response = {
		// 	"list_orders": [
		// 		[
		// 			1,
		// 			"APROVADO",
		// 			"João",
		// 			[
		// 				"misto",
		// 				"x-salada"
		// 			]
		// 		],
		// 		[
		// 			2,
		// 			"APROVADO",
		// 			"Lúcia",
		// 			[
		// 				"misto",
		// 				"hot-dog"
		// 			]
		// 		],
		// 		[
		// 			3,
		// 			"APROVADO",
		// 			"Igor",
		// 			[
		// 				"hot-dog",
		// 				"x-salada"
		// 			]
		// 		],
		// 		[
		// 			4,
		// 			"PROCESSANDO",
		// 			"Lucas",
		// 			[
		// 				"x-salada",
		// 				"misto"
		// 			]
		// 		]
		// 	]
		// }

		var response = resp.data;
		var table = document.getElementById('table_user').getElementsByTagName('tbody')[0];

		// LIMPAMOS O QUE TINHA ANTES e depois inserimos novos itens
		// isso impede que a tabela reexiba os dados seguidamente
		for (i = table.rows.length - 1; i >= 0; i--) {
			table.deleteRow(i);
		}

		for (var i = 0; i < response.list_orders.length; i++) {
			// criar uma nova linha de tabela e insere no começo
			var row = table.insertRow(i);

			// cria duas novas células (id, nome)
			//var cell1 = row.insertCell(0);
			//var cell2 = row.insertCell(1);
			for (var j = 0; j < response.list_orders[i].length; j++) {
				// cria uma nova células (id, nome, e etc...)
				var cell1 = row.insertCell(j);
				// altera o texto da célula (id, nome, e etc...)
				cell1.innerHTML = response.list_orders[i][j];
			}
			var cell1 = row.insertCell(response.list_orders[i].length);
			if (response.list_orders[i][1] == "PROCESSANDO")
				cell1.innerHTML = `<button type="button" class="btn btn-success" onclick=update_order(${response.list_orders[i][0]})>Approve Payment</button>`;
			else
				cell1.innerHTML = `<button type="button" class="btn disabled btn-success" >Approve Payment</button>`;
			var cell2 = row.insertCell(response.list_orders[i].length + 1);
			cell2.innerHTML = `<button type="button" class="btn btn-danger" onclick=delete_order(${response.list_orders[i][0]})>Delete</button>`;

			// segunda posição da linha i => nome
			//cell2.innerHTML = response.list[i][0]
			//cell2.innerHTML = response.list[i][1]

			// print
			console.log(response.list_orders[i]);
		}
	});
}


function post_order() {
	// var table = document.getElementById('table_user')
	var nome = document.getElementById('order_name').value;
	var itens = document.getElementById('order_items').value;

	console.log(nome); // "José"
	console.log(itens); // "1,2,3"

	var order = {
		"nome": nome,
		"items": itens.split(",").map(Number)
	}

	console.log(order);

	// axios.get('https://jsonplaceholder.typicode.com/todos/1').then(resp => {
	// axios.post('https://w0q1zo1lwf.execute-api.localhost.localstack.cloud:4566/api/order', order).then(resp => {
	axios.post('http://localhost:4566/restapis/lbxs8haiad/local/_user_request_/order', order).then(resp => {
		console.log("Cadastrado");
		console.log(resp.data);

		document.getElementById('order_name').value = ""; // LIMPAMOS OS CAMPOS
		document.getElementById('order_items').value = ""; //LIMPAMOS OS CAMPOS

		get_order();
	});
}

function update_order(id) {
	// {
	// 	"ID": "2"
	//  }
	var order = {
		"ID": id
	}
	axios.patch('http://localhost:4566/restapis/lbxs8haiad/local/_user_request_/order', order).then(resp => {
		console.log("APROVADO");

		get_order();
	});
}

function delete_order(id) {
	axios.delete(`http://localhost:4566/restapis/lbxs8haiad/local/_user_request_/order/${id}`).then(resp => {
		console.log("DELETADO");

		get_order();
	});
}

window.onload = setInterval(get_order, 3000);
