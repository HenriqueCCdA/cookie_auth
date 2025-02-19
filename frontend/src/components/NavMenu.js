// React Router
import { NavLink } from "react-router-dom";
// Hooks
import { useAuth } from "../hooks/useAuth";
import { useDispatch } from "react-redux";
// Redux
import { logout } from "../redux/slices/authSlice";

const NavMenu = () => {
  const navLinksNoAuth = [
    { name: "Login", url: "/login" },
    { name: "Cadastro", url: "/register" },
  ];

  const navLinksAuth = [{ name: "Dashboard", url: "/dashboard" }];

  const { auth } = useAuth();
  const dispatch = useDispatch();

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
      <div className="container-fluid">
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {navLinksNoAuth.map(
              ({ name, url }, idx) =>
                !auth && (
                  <li className="nav-item" key={idx}>
                    <NavLink className="nav-link" to={url} end>
                      {name}
                    </NavLink>
                  </li>
                )
            )}
            {navLinksAuth.map(
              ({ name, url }, idx) =>
                auth && (
                  <li className="nav-item" key={idx}>
                    <NavLink className="nav-link" to={url} end>
                      {name}
                    </NavLink>
                  </li>
                )
            )}
          </ul>
        </div>
        <div className="d-flex align-items-center">
          {auth && (
            <button
              className="btn btn-outline-danger btn-sm mx-1"
              onClick={() => dispatch(logout())}
            >
              <span className="d-flex justify-content-center align-items-center">
                Logout
              </span>
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default NavMenu;
