import logo from "./logo.svg";
import "./App.css";
import LoginForm from "./LoginForm";
import ProtectedRoute from "./ProtectedRoute";
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route,
} from "react-router-dom";

const login__ = window.localStorage.getItem("accesstoken");
const routerDefinition = createRoutesFromElements(
  <Route>
    <Route path="/" element={<LoginForm />} />
    <Route path="/login" element={<LoginForm />} />
    <Route
      path="/protectedroute"
      element={login__ ? <ProtectedRoute /> : <LoginForm />}
    />
    {/* <Route path="/protectedroute" element={<ProtectedRoute />} /> */}
  </Route>
);

const router = createBrowserRouter(routerDefinition);
function App() {
  return <RouterProvider router={router} />;
}

export default App;

// function App() {
//   return (
//     <div className="App">
//       <LoginForm />
//       <ProtectedRoutes />
//     </div>
//   );
// }

// export default App;
