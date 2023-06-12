import React, { useEffect, useState, useRef } from 'react';
import PropTypes from 'prop-types';
import ArgonBox from 'components/ArgonBox';
import ArgonTypography from 'components/ArgonTypography';
import ArgonAvatar from 'components/ArgonAvatar';
import ArgonBadge from 'components/ArgonBadge';
import Table from 'examples/Tables/Table';
import { UserContext } from 'UserContext';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';

function Author({ image, name, email }) {
  const formattedImage = image.replace(/ /g, '_');
  return (
    <ArgonBox display="flex" alignItems="center" px={1} py={0.5}>
      <ArgonBox mr={2}>
        <ArgonAvatar src={`${process.env.PUBLIC_URL}/${formattedImage}.png`} alt={name} size="sm" variant="rounded" />
      </ArgonBox>
      <ArgonBox display="flex" flexDirection="column">
        <ArgonTypography variant="button" fontWeight="medium">
          {name}
        </ArgonTypography>
        <ArgonTypography variant="caption" color="secondary">
          {email}
        </ArgonTypography>
      </ArgonBox>
    </ArgonBox>
  );
}

Author.propTypes = {
  image: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  email: PropTypes.string.isRequired,
};

function Function({ job, org }) {
  return (
    <ArgonBox display="flex" flexDirection="column">
      <ArgonTypography variant="caption" fontWeight="medium" color="text">
        {job}
      </ArgonTypography>
      <ArgonTypography variant="caption" color="secondary">
        {org}
      </ArgonTypography>
    </ArgonBox>
  );
}

Function.propTypes = {
  job: PropTypes.string.isRequired,
  org: PropTypes.string.isRequired,
};

const AuthorsTable = () => {
  const [authorsData, setAuthorsData] = useState([]);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(true);
  const { userId, setUserId } = React.useContext(UserContext);
  const tableContainerRef = useRef(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://10.4.41.51:8000/get_transactions?user_id=${userId}&page=${pageNumber}`);
        const data = await response.json();
        setAuthorsData((prevData) => [...prevData, ...data]);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [pageNumber]);

  const handleScroll = () => {
    const element = tableContainerRef.current;
    if (element.scrollTop + element.clientHeight === element.scrollHeight) {
      loadNextPage();
    }
  };

  const loadNextPage = () => {
    setPageNumber((prevPageNumber) => prevPageNumber + 1);
  };

  useEffect(() => {
    const element = tableContainerRef.current;
    if (element) {
      element.addEventListener('scroll', handleScroll);
    }
    return () => {
      if (element) {
        element.removeEventListener('scroll', handleScroll);
      }
    };
  }, []);

  const authorsTableData = {
    columns: [
      { name: 'bank', align: 'center' },
      { name: 'id', align: 'left' },
      { name: 'source bank', align: 'center' },
      { name: 'Transaction date', align: 'center' },
      { name: 'Income/Spent', align: 'center' },
      { name: 'action', align: 'center' },
    ],
    rows: authorsData.map((author) => ({
      bank: <Author image={author.transactionInformation[0]} name={author.proprietaryBankTransactionCode.issuer} email={author.transactionInformation[0]} />,
      id: <Function job={author.id} org={author.amount} />,
      "source bank": (
        <ArgonBadge
          variant="gradient"
          badgeContent={author.transactionInformation[0]}
          color={author.transactionInformation[0] === "income" || author.transactionInformation[0] === "refund" ? 'success' : 'secondary'}
          size="xs"
          container
        />
      ),
      "Transaction date": (
        <ArgonTypography variant="caption" color="secondary" fontWeight="medium">
          {author.date}
        </ArgonTypography>
      ),
      "Income/Spent": (
        <ArgonTypography variant="caption" color="secondary" fontWeight="medium">
          {author.amount > 0 ? author.amount : -1 * author.amount}
        </ArgonTypography>
      ),
      action: (
        <ArgonTypography
          component="a"
          href="#"
          variant="caption"
          color="secondary"
          fontWeight="medium"
        >
          Edit
        </ArgonTypography>
      ),
    })),
  };

  return (
    <div>
      {authorsTableData.rows && authorsTableData.rows.length > 0 ? (
        <div
          ref={tableContainerRef}
          style={{ height: '70vh', overflow: 'auto' }}
          onScroll={handleScroll}
        >
          <Table columns={authorsTableData.columns} rows={authorsTableData.rows} />
          {loading && <div>Loading...</div>}
        </div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
};

export default AuthorsTable;
