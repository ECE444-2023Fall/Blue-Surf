import axios from "axios";

function Header(props) {

  function logMeOut() {
    axios({
      method: "POST",
      url:"/logout",
    })
    .then((response) => {
       props.token()
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

    return(
        <header className="App-header">
            {/*<img src={logo} className="App-logo" alt="logo" />
            <button onClick={logMeOut}> 
                Logout
    </button>*/}
        </header>
    )
}

export default Header;
