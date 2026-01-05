import "../styles/Alert.css";

interface AlertProps{
    type: "success" | "error" | "info";
    message: string;
    icon: string;
}
export default function Alert({type,message,icon}: AlertProps){
    return(
        <div className = {`alert alert-${type}`}>
            <span className = "alert-icon">{icon}</span>
            <span>{message}</span>
        </div>
    )
}