import {createHashRouter} from "react-router-dom";
import ErrorPage from "./pages/error/Error";
import * as React from "react";
import {Login} from "./pages/login/Login";
import {Auth} from "./layouts/Auth";
import SignUp from "./pages/signup/SignUp";
import {ChatFlow} from "./pages/chatflow";
import {Admin} from "./layouts/Admin";
import {HomeFlow} from "./pages/home";

export const router = createHashRouter([
    {
        path: "/",
        element: <Auth/>,
        errorElement: <ErrorPage/>,
        children: [
            {
                path: "",
                element: <SignUp/>,
            },
            {
                path: "/homeflow",
                element: <HomeFlow/>,
            },
            {
                path: "login",
                element: <Login/>
            },
            {
                path: "signup",
                element: <SignUp/>
            }
        ],
    },
    {
        path: "/chatflow",
        element:<Admin/>,
        errorElement: <ErrorPage/>,
        children: [
            {
                path: "",
                element: <ChatFlow/>,
            }
        ],
    }
]);
