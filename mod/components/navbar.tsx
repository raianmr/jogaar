import Link from "next/link"

export default function Navbar() {
  return (
    <div>
      <nav className="navbar navbar-expand-md navbar-dark bg-dark mb-4">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Jogaar Mods
          </a>
          <div>
            <ul className="navbar-nav me-auto mb-2 mb-md-0">
              <li className="nav-item">
                <Link className="nav-link" href="/dashboard">
                  Dashboard
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" href="/login">
                  Login
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  )
}
