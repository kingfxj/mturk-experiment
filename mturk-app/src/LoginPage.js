import React from "react";
import "./LoginPage.css";
import clsx from "clsx";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import InputAdornment from "@material-ui/core/InputAdornment";
import FormControl from "@material-ui/core/FormControl";
import Visibility from "@material-ui/icons/Visibility";
import VisibilityOff from "@material-ui/icons/VisibilityOff";
import Button from "@material-ui/core/Button";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexWrap: "wrap",
  },
  margin: {
    margin: theme.spacing(1),
  },
  withoutLabel: {
    marginTop: theme.spacing(3),
  },
  textField: {
    width: "25ch",
  },
  button: {
    margin: theme.spacing(1),
  },
}));

export const LoginPage = () => {
  const classes = useStyles();
  const [values, setValues] = React.useState({
    username: "",
    password: "",
    showPassword: false,
  });

  const handleChange = (prop) => (event) => {
    setValues({ ...values, [prop]: event.target.value });
  };

  const handleClickShowPassword = () => {
    setValues({ ...values, showPassword: !values.showPassword });
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <div className="login">
      <div>
        <h2 style={{ color: "#f50057" }}>SIGN IN</h2>
      </div>
      <div>
        <FormControl className={clsx(classes.margin, classes.textField)}>
          <InputLabel color="secondary" htmlFor="standard-adornment-username">
            Username
          </InputLabel>
          <Input
            id="standard-adornment-username"
            value={values.username}
            color="secondary"
            onChange={handleChange("username")}
          />
        </FormControl>
      </div>
      <div>
        <FormControl className={clsx(classes.margin, classes.textField)}>
          <InputLabel color="secondary" htmlFor="standard-adornment-password">
            Password
          </InputLabel>
          <Input
            id="standard-adornment-password"
            type={values.showPassword ? "text" : "password"}
            value={values.password}
            color="secondary"
            onChange={handleChange("password")}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                >
                  {values.showPassword ? <Visibility /> : <VisibilityOff />}
                </IconButton>
              </InputAdornment>
            }
          />
        </FormControl>
      </div>
      <div>
        <br></br>
        <Button
          variant="contained"
          color="secondary"
          className={classes.button}
        >
          LOGIN
        </Button>
      </div>
    </div>
  );
};
