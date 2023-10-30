import React from "react";
import { Route, Routes } from "react-router-dom";
import { useContext } from "react";
import PostCreation from "./components/PostCreation";
export const AppRouter = () => {
    return (
        <Routes>

            <Route path="/postcreation" element={<PostCreation />}></Route>
            {/*<Route path="/login" element={<Login />}></Route>
            <Route path="/signup" element={<SignUp />}></Route> */} 
    </Routes> 
)
}
