
import './App.css'
import Landing from "./Components/Landing.jsx";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import SoilAnalysis from "./Components/SoilAnalysis.jsx";
import WeatherPrediction from "./Components/WeatherPrediction.jsx";

function App() {

    const appRouter=createBrowserRouter([
        {
            path: "/",
            element: <Landing/>
        },
        {
            path:"/soil",
            element: <SoilAnalysis/>
        },
        {
            path:"/weather",
            element: <WeatherPrediction/>
        }
    ])
  return (
    <div>
        <RouterProvider router={appRouter}>
        </RouterProvider>
    </div>
  )
}

export default App;