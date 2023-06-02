import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import ArgonBox from 'components/ArgonBox';
import ArgonTypography from 'components/ArgonTypography';
import ArgonAvatar from 'components/ArgonAvatar';
import ArgonBadge from 'components/ArgonBadge';
import team2 from 'assets/images/team-2.jpg';
import team3 from 'assets/images/team-3.jpg';
import team4 from 'assets/images/team-4.jpg';
import Table from "examples/Tables/Table"
import { UserContext } from 'UserContext';


function Author({ image, name, email }) {
  return (
    <ArgonBox display="flex" alignItems="center" px={1} py={0.5}>
      <ArgonBox mr={2}>
        <ArgonAvatar src={image} alt={name} size="sm" variant="rounded" />
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
  const { userId, setUserId } = React.useContext(UserContext);
  console.log('User ID:', userId);
  useEffect(() => {
    // Fetch data from the API
    const fetchData = async () => {
      try {
        const response = await fetch('http://10.4.41.51:8000/get_transactions?user_id='+userId);
        const data = await response.json();
        console.log(data);
        setAuthorsData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const authorsTableData = {
    columns: [
      { name: 'bank', align: 'center' },
      { name: 'id', align: 'left' },
      { name: 'source bank', align: 'center' },
      { name: 'Transaction date', align: 'center' },
      { name: 'action', align: 'center' },
    ],
    rows: authorsData.map((author) => ({
      bank: <Author image={author.image} name={author.proprietaryBankTransactionCode.issuer} email={author.transactionInformation[0]} />,
      id: <Function job={author.id} org={author.amount} />,
      "source bank": (
        <ArgonBadge
          variant="gradient"
          badgeContent={author.proprietaryBankTransactionCode.issuer}
          color={author.proprietaryBankTransactionCode.issuer === 'BNP PARIBAS' ? 'success' : 'secondary'}
          size="xs"
          container
        />
      ),
      "Transaction date": (
        <ArgonTypography variant="caption" color="secondary" fontWeight="medium">
          {author.date}
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
        // Render your table using the authorsTableData
        <div>
         <Table columns={authorsTableData.columns} rows={authorsTableData.rows} />
        </div>
      ) : (
        // Render a loading state or an empty state if no data is available
        <div>Loading...</div>
      )}
    </div>
  );
};

export default AuthorsTable;
