package cats.coding.istalku;

import android.*;
import android.app.*;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.media.RingtoneManager;
import android.os.Bundle;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.provider.Settings;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.PendingResult;
import com.google.android.gms.common.api.ResultCallback;
import android.util.Log;
import android.widget.Toast;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

import java.io.IOException;
import java.util.Calendar;
import java.util.concurrent.Executor;

/**
 * Created by sungeee on 11/7/17.
 */

public class ForegroundService extends Service{
    private LocationListener locListener;
    private LocationManager locManager;
//    private Boolean running = false;
    private String provider;
    private String myLat = "-1";
    private String myLng = "-1";
    String mSteps = "";
    Notification.Builder builder;
    Storage storage;


    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onCreate() {
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        storage = new Storage(getApplicationContext());

        if (intent != null && intent.getAction() == "STOP"){
            SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
            sp.edit().putBoolean("track", false).apply();
            stopService(intent);
            }
        else{
            // Set up a new location listener.
            initiateNotification();
            reRegisterSensor();
            SharedPreferences sp = PreferenceManager.getDefaultSharedPreferences(this);
            locListener = new LocationListener() {

                // along with a gps update, append to the file a time stamp and a lat lng
                @Override
                public void onLocationChanged(Location location) {
                    myLat = String.valueOf(location.getLatitude());
                    myLng = String.valueOf(location.getLongitude());
                    Log.d("debug", myLat + ", " + myLng);
                    Calendar calendar = Calendar.getInstance();
                    storage.writeToFile(calendar, myLat, myLng);
                    Intent update = new Intent();
                    update.setAction("UPDATE");
                    sendBroadcast(update);
                    initiateNotification();
                }

                @Override
                public void onStatusChanged(String s, int i, Bundle bundle) {

                }

                @Override
                public void onProviderEnabled(String s) {

                }

                @Override
                public void onProviderDisabled(String s) {
                    Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                    startActivity(intent);
                }
            };

            locManager = (LocationManager) getSystemService(LOCATION_SERVICE);
            provider = locManager.getBestProvider(new Criteria(), false);
            try {
                // retrieve from the shared preference the stored gps frequency value, and request location update in correspondence to the frequency value
                locManager.requestLocationUpdates(provider, sp.getInt("gps_freq", 1000), 3, locListener);
                Log.d("gps_freq", String.valueOf(sp.getInt("gps_freq", 0)));
            } catch (SecurityException e) {
                Log.d("ERROR", "Permission Not Granted");
            }
        }
        return super.onStartCommand(intent, flags, startId);
    }

    // when start the service, initiate a notification
    public void initiateNotification(){
        NotificationManager nm = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        builder = new Notification.Builder(this);

        Intent notiIntent = new Intent(this, Menu.class);
        notiIntent.putExtra("fileName", storage.getFileName(Calendar.getInstance()));
        notiIntent.setAction("NOTI");
        notiIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pi = PendingIntent.getActivity(this, 0, notiIntent, 0);

        Intent stopIntent = new Intent(this, ForegroundService.class);
        stopIntent.setAction("STOP");
        PendingIntent stopPi = PendingIntent.getService(this, 0, stopIntent, 0);
        Notification.Action stopAction = new Notification.Action.Builder(null, "STOP", stopPi).build();

        Notification noti = builder.setContentTitle("I am watching you")
                .setSmallIcon(R.drawable.bino_small)
                .setContentIntent(pi)
                .setContentText("Latitude : " + myLat + " | Longitude : " + myLng + " | Steps : " + mSteps)
                .addAction(stopAction)
                .setOngoing(true).build();

        startForeground(1, noti);
    }

    // When it gets destroyed make sure to get rid of the Location Listener.
    @Override
    public void onDestroy() {
        super.onDestroy();
        Intent stopIntent = new Intent();
        stopIntent.setAction("STOP SERVICE");
        sendBroadcast(stopIntent);
        if (locManager != null){
            Log.d("DEBUG", "destroyed");
            locManager.removeUpdates(locListener);
        }
    }

    /**
     * Listener that handles step sensor events for step detector and step counter sensors.
     */
    private final SensorEventListener mListener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            Calendar calendar = Calendar.getInstance();
            storage.recordStepIncrement(calendar);
            mSteps = String.valueOf(storage.readSteps(storage.getFileName(calendar)+"_steps"));
            initiateNotification();
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {

        }
    };

    private void reRegisterSensor() {
        SensorManager sm =
                (SensorManager) this.getSystemService(Activity.SENSOR_SERVICE);
        try {
            //sm.unregisterListener();
        } catch (Exception e) {
            e.printStackTrace();
        }

        Log.d("sensor","step sensors: " + sm.getSensorList(Sensor.TYPE_STEP_DETECTOR).size());

        // enable batching with delay of max 5 min
        sm.registerListener(mListener, sm.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR),
                SensorManager.SENSOR_DELAY_NORMAL, (5 * 60 * 1000));
    }
}
