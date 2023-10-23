import {Navigate, useLocation} from 'react-router-dom'
import {SessionManager} from "../../domain/session/SessionManager";

export function RequiresAuth({children}: { children: JSX.Element }): JSX.Element {
    const user = SessionManager.getInstance().getSessionData().token
    console.log("user", user)
    const location = useLocation()
    if (!user) {
        return <Navigate to="/login" state={{from: location}} replace/>
    }
    return children
}
