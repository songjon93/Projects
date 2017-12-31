package cats.coding.istalku;

import android.content.Context;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Calendar;
import android.util.Log;

import java.io.FileOutputStream;
import java.io.IOException;


/**
 * Created by liaos on 11/17/2017.
 */

public class Storage {

    private static final String TAG = "Storage";
    private static final String COMMA = ",";

    private final Context context;

    public Storage(Context context) {
        this.context = context;
    }

    // Given a calendar instance, write a new line of time, lat value, and lng value to a file named after the date
    public void writeToFile(Calendar calendar, String latitude, String longitude){
        try {
            String filename = getFileName(calendar);
            FileOutputStream fileOutputStream = context.openFileOutput(filename, context.MODE_APPEND);
            String timestamp = makeTimestamp(calendar);
            Log.d("timestamp", timestamp);
            fileOutputStream.write(timestamp.getBytes());
            fileOutputStream.write(COMMA.getBytes());
            fileOutputStream.write(latitude.getBytes());
            fileOutputStream.write(COMMA.getBytes());
            fileOutputStream.write(longitude.getBytes());
            fileOutputStream.write("\n".getBytes());

            fileOutputStream.close();
        } catch (IOException e) {
            Log.d(TAG, e.toString());
        }
    }

    // returns a file name using the calendar instance
    public String getFileName(Calendar calendar){
        String date = "";
        date += String.valueOf(calendar.get(Calendar.YEAR));
        date += String.valueOf(calendar.get(Calendar.MONTH) + 1);
        date += String.valueOf(calendar.get(Calendar.DATE));
        return date;
    }

    // read through the file, store the values to a data object and return a sorted array of the data objects.
    public ArrayList<Data> readFile(String fileName){
        ArrayList<Data> dataList = new ArrayList<>();
        try{
            FileInputStream fis = context.openFileInput(fileName);
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader bufferedReader = new BufferedReader(isr);
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                String[] data = line.split(",");
                if (data.length == 3) {
                    Data newData = new Data(data[0], data[1], data[2]);
                    dataList.add(newData);
                }
            }
            isr.close();
            fis.close();
        } catch (IOException e){
                Log.d("Error", e.toString());
                return null;
        }
        return dataList;
    }

    // Make a timestamp given a calendar instance
    public String makeTimestamp(Calendar calendar) {
        String timestamp = "";
        timestamp += String.format("%02d", calendar.get(Calendar.HOUR_OF_DAY));
        timestamp += String.format("%02d", calendar.get(Calendar.MINUTE));
        timestamp += String.format("%02d", calendar.get(Calendar.SECOND));
        Log.d("debug", timestamp);

        return timestamp;
    }

    // At every step taken, read the value written in the file, and update it by incrementing the value by 1.
    public void recordStepIncrement(Calendar calendar) {
        String filename = getFileName(calendar) + "_steps";
        try{
            int steps = readSteps(filename);
            steps += 1;

            FileOutputStream fileOutputStream = context.openFileOutput(filename, context.MODE_PRIVATE);
            fileOutputStream.write(String.valueOf(steps).getBytes());
            fileOutputStream.close();

            Log.d("recordStepIncrement", "steps: " + steps);
        } catch (IOException e) {
            Log.d(TAG, e.toString());
        }
    }

    // read in the step file and return the total number of steps taken.
    public int readSteps(String filename) {
        try {
            FileInputStream fis = context.openFileInput(filename);
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader bufferedReader = new BufferedReader(isr);
            String line;
            line = bufferedReader.readLine();

            int steps = Integer.parseInt(line);
            Log.d("recordStep", String.valueOf(steps));
            isr.close();
            fis.close();

            return steps;
        } catch (IOException e) {
            Log.d(TAG, e.toString());
        }
        Log.d("readSteps", "Failed to read: " + filename);
        return 0;
    }
}
