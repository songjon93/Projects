package cats.coding.istalku;

import android.Manifest;
import android.app.DialogFragment;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationManager;
import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.support.annotation.Nullable;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.NumberPicker;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.MapsInitializer;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class TimeMachine extends Fragment{
    MapView mView;
    SeekBar timeView;
    private GoogleMap gMap;
    private ArrayList<LatLng> locations = new ArrayList<>();
    private Marker curMarker = null;
    static Menu curActivity;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_time_machine, container, false);
        curActivity = (Menu) getActivity();
        timeView = view.findViewById(R.id.timeView);
        if(curActivity.dataList != null) setListener();
        mView = (MapView) view.findViewById(R.id.mapView);
        mView.onCreate(savedInstanceState);
        mView.onResume();

        try{
            MapsInitializer.initialize(getActivity().getApplicationContext());
        } catch (Exception e){
            Log.d("Error", e.toString());
        }

        mView.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(GoogleMap googleMap) {
                gMap = googleMap;
                if (curActivity.dataList != null) drawPath();
            }
        });
        return view;
    }

    // Draw path between two locations in correspondence to the time line
    public void drawPath(){
        PolylineOptions line = new PolylineOptions();
        line.color(Color.RED);
        int len = curActivity.dataList.size();
        for (int i = 1; i < len; i++) {
            line.add(getLatLng(i - 1), getLatLng(i));
        }
        gMap.addPolyline(line);
        drawMarker(0);
        gMap.moveCamera(CameraUpdateFactory.newLatLng(getLatLng(0)));
        gMap.moveCamera(CameraUpdateFactory.zoomTo(15.5f));
    }

    // In accordance with the seek bar value, draw a marker on the map
    public void drawMarker(int index){
        if (curMarker != null) curMarker.remove();
        LatLng pos = getLatLng(index);
        curMarker = gMap.addMarker(new MarkerOptions().position(pos));
        curMarker.setTitle("Your Location");
        curMarker.setSnippet(getTime(index));
        gMap.moveCamera(CameraUpdateFactory.newLatLng(getLatLng(index)));
    }

    // Construct a time string for the marker snippet
    public String getTime(int index){
        String timestamp = "at ";
        String before = curActivity.dataList.get(index).getTime();
        timestamp += before.substring(0, 2) + " : ";
        timestamp += before.substring(2, 4) + " : ";
        timestamp += before.substring(4, 6);

        return timestamp;
    }

    // Turn stored string data into Latlng format
    public LatLng getLatLng(int index){
        Data datum = curActivity.dataList.get(index);
        return new LatLng(Float.valueOf(datum.getLat()), Float.valueOf(datum.getLng()));

    }

    public void showQuery(View view){
        QueryDialog query = new QueryDialog();
        query.show(getFragmentManager(), "query");
    }
    public void search(String time){
        if (curActivity.dataList == null) return;
        Long minDiff = Long.MAX_VALUE;
        int index = 0;
        int min_index = 0;
        for (Data datum : curActivity.dataList) {
            try {
                SimpleDateFormat format = new SimpleDateFormat("HHmmss");
                Date date1 = format.parse(time+"00");
                Date date2 = format.parse(datum.getTime());

                Long diff = Math.abs(date2.getTime() - date1.getTime());
                Log.d("time_ diff", String.valueOf(diff));
                if (diff < minDiff){
                    minDiff = diff;
                    min_index = index;
                }
            } catch (ParseException e){
                Log.d("Error", e.toString());
            }
            index++;
        }
        if (minDiff > 3600000) {
            if(this != null) Toast.makeText(getContext(), "Your location was not found for requested time", Toast.LENGTH_SHORT).show();
        } else {
            drawMarker(min_index);
            timeView.setProgress(min_index);
            if(this != null) Toast.makeText(getContext(), "Search Complete", Toast.LENGTH_SHORT).show();
        }
    }

    public void setListener(){
        timeView.setMax(curActivity.dataList.size() - 1);
        timeView.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                drawMarker(i);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
            }
        });
    }

    @Override
    public void onResume() {
        super.onResume();
        mView.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
        mView.onPause();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        mView.onDestroy();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
        mView.onLowMemory();
    }

    public static class QueryDialog extends DialogFragment {
        NumberPicker hours, mins;
        TextView search;
        TimeMachine parent;
        Fragment cur;

        @Nullable
        @Override
        public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
            View v = inflater.inflate(R.layout.query, container, false);
            cur = this;
            parent = (TimeMachine) curActivity.fragments.get(2);
            search = v.findViewById(R.id.search);
            hours = v.findViewById(R.id.hours);
            mins = v.findViewById(R.id.minutes);

            initialize_picker();
            startListener();
            return v;
        }

        public void initialize_picker(){
            hours.setMinValue(0);
            hours.setMaxValue(23);
            mins.setMinValue(0);
            mins.setMaxValue(59);
        }

        public void startListener(){
            search.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    parent.search(String.format("%02d", hours.getValue()) + String.format("%02d", mins.getValue()));
                    parent.getFragmentManager().beginTransaction().remove(cur).commit();
                }
            });
        }
    }
}
