const form = document.querySelector('#form');
const tbody = document.querySelector('#tbody');
const total = document.querySelector('#total');

// Função para excluir um produto
const deleteProduct = (id, row) => {
  console.log('Deleting product with ID', id);
  fetch(`/api/products/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log('Product deleted successfully');
      row.remove();
      const currentTotal = parseFloat(total.textContent) || 0;
      total.textContent = currentTotal - (data.product.quantity * data.product.price);
      addDeleteListeners();
    } else {
      console.error('Error deleting product:', data.error);
      alert(data.error);
    }
  })
  .catch(error => console.error(error));
};

const addDeleteListeners = () => {
  const deleteButtons = document.querySelectorAll('.delete');
  deleteButtons.forEach(deleteButton => {
    console.log('Adding click listener for delete button with ID', deleteButton.getAttribute('data-id'));
    deleteButton.addEventListener('click', () => {
      const id = deleteButton.getAttribute('data-id');
      const row = deleteButton.parentNode.parentNode;
      console.log('Deleting product with ID', id);
      deleteProduct(id, row);
    });
  });
};

fetch('/api/products')
  .then(response => response.json())
  .then(data => {
    data.products.forEach(product => {
      const row = `
        <tr>
          <td>${product.name}</td>
          <td>${product.quantity}</td>
          <td>${product.price}</td>
          <td>${product.quantity * product.price}</td>
          <td>
            <button class="delete" data-id="${product.id}">Excluir</button>
          </td>
        </tr>
      `;
      tbody.insertAdjacentHTML('beforeend', row);
    });

    addDeleteListeners();
  })
  .catch(error => console.error(error));

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = document.querySelector('#productName').value;
  const quantity = document.querySelector('#productQuantity').value;
  const price = document.querySelector('#productPrice').value;

  fetch('/api/products', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name,
      quantity,
      price
    })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const product = data.product;
        const row = `
          <tr>
            <td>${product.name}</td>
            <td>${product.quantity}</td>
            <td>${product.price}</td>
            <td>${product.quantity * product.price}</td>
            <td>
              <button class="delete" data-id="${product.id}">Excluir</button>
            </td>
          </tr>
        `;
        tbody.insertAdjacentHTML('beforeend', row);

        const currentTotal = parseFloat(total.textContent) || 0;
        total.textContent = currentTotal + (product.quantity * product.price);

        document.querySelector('#productName').value = '';
        document.querySelector('#productQuantity').value = '';
        document.querySelector('#productPrice').value = '';

        addDeleteListeners();
      } else {
        alert(data.error);
      }
    })
    .catch(error => console.error(error));
});

addDeleteListeners();