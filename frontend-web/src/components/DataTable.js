import React from "react";

const DataTable = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="data-table">
      <h3>📋 Equipment Data Table</h3>
      <table>
        <thead>
          <tr>
            <th>Equipment Name</th>
            <th>Type</th>
            <th>Flowrate</th>
            <th>Pressure</th>
            <th>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.equipment_name}</td>
              <td>{item.equipment_type}</td>
              <td>{item.flowrate.toFixed(2)}</td>
              <td>{item.pressure.toFixed(2)}</td>
              <td>{item.temperature.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
