import React, { useState, forwardRef } from "react";
import MaterialTable from "material-table";
import ArrowDownward from "@material-ui/icons/ArrowDownward";
import Check from "@material-ui/icons/Check";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Clear from "@material-ui/icons/Clear";
import DeleteOutline from "@material-ui/icons/DeleteOutline";
import Edit from "@material-ui/icons/Edit";
import FilterList from "@material-ui/icons/FilterList";
import FirstPage from "@material-ui/icons/FirstPage";
import LastPage from "@material-ui/icons/LastPage";
import Remove from "@material-ui/icons/Remove";
import Search from "@material-ui/icons/Search";
import ViewColumn from "@material-ui/icons/ViewColumn";
import LocalAtmIcon from "@material-ui/icons/LocalAtm";

// icons
const tableIcons = {
  Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
  Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
  DetailPanel: forwardRef((props, ref) => (
    <ChevronRight {...props} ref={ref} />
  )),
  Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
  Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
  FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
  LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
  NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
  PreviousPage: forwardRef((props, ref) => (
    <ChevronLeft {...props} ref={ref} />
  )),
  ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
  Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
  SortArrow: forwardRef((props, ref) => <ArrowDownward {...props} ref={ref} />),
  ThirdStateCheck: forwardRef((props, ref) => <Remove {...props} ref={ref} />),
  ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />),
  LocalAtmIcon: forwardRef((props, ref) => (
    <LocalAtmIcon {...props} ref={ref} />
  )),
};

// set assignments variables
export const AssignmentsPage = () => {
  const [columns, setColumns] = useState([
    { title: "Name", field: "name" },
    {
      title: "Surname",
      field: "surname",
    },
    { title: "Birth Year", field: "birthYear", type: "numeric" },
    {
      title: "Birth Place",
      field: "birthCity",
    },
  ]);

  // set data from variables (temporary data)
  const [data, setData] = useState([
    {
      name: "Jonathan",
      surname: "issaGod",
      birthYear: 1987,
      birthCity: "Edmonton",
    },
    {
      name: "Ildar",
      surname: "issaGod",
      birthYear: 2020,
      birthCity: "Calgary",
    },
  ]);

  // return material table with given data
  return (
    data && data.length > 0 && data.map((item) => <p>{item.about}</p>),
    (
      <MaterialTable
        icons={tableIcons}
        title="Assignments"
        columns={columns}
        data={data}
        // filtering/selection option + table styles
        options={{
          filtering: true,
          selection: true,
          headerStyle: {
            backgroundColor: "#a5bddd",
            color: "black",
            fontSize: 20,
            textAlign: "center",
          },
          cellStyle: {
            fontSize: 15,
            textAlign: "center",
          },
        }}
        // pay option
        actions={[
          {
            tooltip: "Pay Selected Users",
            icon: LocalAtmIcon,
            onClick: (evt, data) =>
              alert("You want to pay " + data.length + " Turkers!"),
          },
        ]}
        // preview/additional info on assignments
        detailPanel={[
          {
            tooltip: "Show/Hide",
            render: (rowData) => {
              return (
                <div
                  style={{
                    fontSize: 40,
                    textAlign: "center",
                    color: "black",
                    backgroundColor: "#a5bddd",
                  }}
                >
                  {rowData.name} {rowData.surname}
                </div>
              );
            },
          },
        ]}
        // edit assignments row option
        editable={{
          onRowUpdate: (newData, oldData) =>
            new Promise((resolve, reject) => {
              setTimeout(() => {
                const dataUpdate = [...data];
                const index = oldData.tableData.id;
                dataUpdate[index] = newData;
                setData([...dataUpdate]);

                resolve();
              }, 1000);
            }),
        }}
      />
    )
  );
};
