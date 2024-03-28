import 'react-notifications/lib/notifications.css';
import {NotificationManager } from 'react-notifications';

export const Notifications = (type,message,title,time) => {
    return () => {
        switch (type) {
            case 'info':
                NotificationManager.info(message, title, time);
                break;
            case 'success':
                NotificationManager.success(message, title, time);
                break;
            case 'warning':
                NotificationManager.warning(message, title, time);
                break;
            case 'error':
                NotificationManager.error(message, title, time);
                break;
            default:
                console.log(`Unexpected Value${type}`)
        }
    };
}