import React from 'react';
// material-ui components
import withStyles from "material-ui/styles/withStyles";
// material-ui icons
import Person from "material-ui-icons/Person";
import Edit from "material-ui-icons/Edit";
import Close from "material-ui-icons/Close";
import KeyboardArrowRight from "material-ui-icons/KeyboardArrowRight";
// core components
import Table from "../../components/Table/Table.jsx";
import Button from "../../components/CustomButtons/Button.jsx";

function Items({...props}){
  const { classes } = props;
  const buttons = [
    { color: "info", icon: Person },
    { color: "success", icon: Edit },
    { color: "danger", icon: Close }
  ].map((prop, key) => {
    return (
      <Button color={prop.color} key={key}>
        {/*<prop.icon className={classes.icon} />*/}
      </Button>
    );
  });
  return (
    <Table
      tableHead={["#","Name","Job Position","Since","Salary","Actions"]}
      tableData={[["1","Andrew Mike","Develop","2013","€ 99,225",buttons]]}
      // customCellClasses={[
      //   classes.center,
      //   classes.right,
      //   classes.right
      // ]}
      // 0 is for classes.center, 4 is for classes.right, 5 is for classes.right
      // customClassesForCells={[0, 4, 5]}
      // customHeadCellClasses={[
      //   classes.center,
      //   classes.right,
      //   classes.right
      // ]}
      // 0 is for classes.center, 4 is for classes.right, 5 is for classes.right
      customHeadClassesForCells={[0, 4, 5]}
    />
  );
}

export default Items;