import React from 'react';
import { Table } from 'react-bootstrap';
import { Helmet } from 'react-helmet';

const jsonData = [
  {
    id: 1,
    item: 'Super Thin Soap 1 Box',
    name: 'Mark',
    badge: 'Regular',
    email: 'mark@mail.com',
    status: 'Shipped',
    amount: 'NT$ 899',
  },
  {
    id: 2,
    item: '(Guaranteed) Bubble-free Body Wash 5 Cans',
    name: 'Jacob',
    badge: 'Regular',
    email: 'jacob@mail.com',
    status: 'Out of Stock',
    amount: 'NT$ 3,600',
  },
  {
    id: 3,
    item: 'Anti-Slip Lampshade 100 Pieces',
    name: 'Larry',
    badge: '',
    email: 'larry@mail.com',
    status: 'Shipped',
    amount: 'NT$ 14,060',
  },
  // Add more JSON data here if needed
];

const TableComponent = () => {
  return (
    <>
    <Helmet>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.9.0/css/all.css" />
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
      integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"
      crossorigin="anonymous"
    />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.css" />
  </Helmet>
    <Table striped bordered hover className="table">
      <thead>
        <tr>
          <th>#</th>
          <th>Item</th>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
          <th>Amount</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {jsonData.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            <td>{item.item}</td>
            <td>
              {item.name}{' '}
              {item.badge && <span className="badge bg-success text-white">{item.badge}</span>}
            </td>
            <td>{item.email}</td>
            <td>{item.status}</td>
            <td>{item.amount}</td>
            <td>
              <div className="btn-group">
                <a href="#" className="btn btn-outline-secondary">Edit</a>
                <a href="#" className="btn btn-outline-secondary">View</a>
                <div className="dropdown">
                  <a href="#" className="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown">...</a>
                  <div className="dropdown-menu">
                    <a href="#" className="dropdown-item">Action History</a>
                    <a href="#" className="dropdown-item">Export Data</a>
                    <div className="dropdown-divider"></div>
                    <a href="#" className="dropdown-item text-danger">Delete Order</a>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
    <nav aria-label="Page navigation example">
        <ul className="pagination d-flex justify-content-center">
          <li className="page-item">
            <a className="page-link" href="#">Previous</a>
          </li>
          <li className="page-item">
            <a className="page-link" href="#">1</a>
          </li>
          <li className="page-item">
            <a className="page-link" href="#">2</a>
          </li>
          <li className="page-item">
            <a className="page-link" href="#">3</a>
          </li>
          <li className="page-item">
            <a className="page-link" href="#">Next</a>
          </li>
        </ul>
      </nav>

      <footer className="py-3 bg-light text-secondary">
        <div className="h6 text-center">I am testing</div>
      </footer>


      <Helmet>
      <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.js"></script>
        {/* <script>
          {`
          $(document).ready(function () {
            $(function () {
              $('[data-toggle="tooltip"]').tooltip()
            })
            $('#editModal').on('show.bs.modal', function (e) {
              var btn = $(e.relatedTarget);
              var title = btn.data('title');
              var modal = $(this);
              modal.find('.modal-title').text(title);
            })
            $('#removeModal').on('show.bs.modal', function (e) {
              var btn = $(e.relatedTarget);
              var title = btn.data('title');
              var modal = $(this);
              modal.find('.modal-title').text(title)
            })
          });
          `}
        </script> */}
      </Helmet>
    </>
  );
};

export default TableComponent;