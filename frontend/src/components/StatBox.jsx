import React from 'react';

function StatBox({ title, value }) {
  return (
    <div className="stat-box">
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

export default StatBox;
