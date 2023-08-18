import {createHashRouter} from "react-router-dom";
import ErrorPage from "./pages/error/Error";
import * as React from "react";
import {Login} from "./pages/login/Login";
import {Home} from "./pages/landingpage/Home";
import {Auth} from "./layouts/Auth";
import SignUp from "./pages/signup/SignUp";
import {FrontChatbot} from "./pages/chatbot";
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
                element: <HomeFlow/>,
            },
            {
                path: "products/chatflow",
                element: <Home/>,
            },
            {
                path: "login",
                element: <Login/>
            },
            {
                path: "signup",
                element: <SignUp/>
            },
            {
                path: "chatbot",
                element: <FrontChatbot/>
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
