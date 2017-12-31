package cats.coding.istalku;

import android.app.DialogFragment;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.app.Fragment;
import android.preference.PreferenceManager;
import android.support.annotation.Nullable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.NumberPicker;
import android.widget.ProgressBar;
import android.widget.TextView;


public class Home extends Fragment {
    static Menu curActivity;
    static int type;
    static final int DIST = 0;
    static final int STEP = 1;
    static final int SPEED = 2;
    static SharedPreferences sp;
    static ProgressBar curBar;

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home, container, false);
        curActivity = (Menu) getActivity();
        sp = PreferenceManager.getDefaultSharedPreferences(getContext());
        updateValue(view);
        return view;
    }

    // Initialize the distance progress bar
    public void setGoalDistance(View view){
        GoalDialog frag = new GoalDialog();
        type = DIST;
        curBar = getView().findViewById(R.id.distanceProgressBar);
        frag.show(getFragmentManager(), "dist");
    }

    // Initialize the step progress bar
    public void setGoalStep(View view){
        GoalDialog frag = new GoalDialog();
        type = STEP;
        curBar = getView().findViewById(R.id.stepProgressBar);
        frag.show(getFragmentManager(), "step");
    }

    // initialize the speed progress bar
    public void setGoalSpeed(View view){
        GoalDialog frag = new GoalDialog();
        type = SPEED;
        curBar = getView().findViewById(R.id.speedProgressBar);
        frag.show(getFragmentManager(), "speed");
    }

    // update the progress bar with the newly updated maximum value and progress value
    public void updateValue(View view){
        ProgressBar progressBar = view.findViewById(R.id.distanceProgressBar);
        progressBar.setMax(sp.getInt(String.valueOf(DIST), 1));
        progressBar.setProgress((int)curActivity.totalDist);
        ((TextView)view.findViewById(R.id.distance_text)).setText(String.valueOf(progressBar.getProgress()) + "/" + String.valueOf(progressBar.getMax()));
        progressBar = view.findViewById(R.id.stepProgressBar);
        progressBar.setMax(sp.getInt(String.valueOf(STEP), 1));
        progressBar.setProgress(curActivity.mSteps);
        ((TextView)view.findViewById(R.id.steps_text)).setText(String.valueOf(progressBar.getProgress()) + "/" + String.valueOf(progressBar.getMax()));
        progressBar = view.findViewById(R.id.speedProgressBar);
        progressBar.setMax(sp.getInt(String.valueOf(SPEED), 1));
        progressBar.setProgress((int)curActivity.max_speed);
        ((TextView)view.findViewById(R.id.speed_text)).setText(String.valueOf(progressBar.getProgress()) + "/" + String.valueOf(progressBar.getMax()));
    }

    @Override
    public void onResume() {
        super.onResume();
    }

    @Override
    public void onPause() {
        super.onPause();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Override
    public void onLowMemory() {
        super.onLowMemory();
    }

    // Goal Dialog is a number picker dialog that lets the user set their progress goal
    public static class GoalDialog extends DialogFragment{
        NumberPicker goal;
        TextView done;
        Home parent;
        Fragment cur;

        int max;
        @Nullable
        @Override
        public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
            View v = inflater.inflate(R.layout.number_picker, container, false);
            cur = this;
            parent = (Home) curActivity.fragments.get(0);
            TextView unit = v.findViewById(R.id.unit);
            goal = v.findViewById(R.id.goal);
            done = v.findViewById(R.id.done);
            switch (type) {
                case DIST:
                    unit.setText(" km");
                    max = 1000;
                    break;
                case STEP:
                    unit.setText(" steps");
                    max = 100000;
                    break;
                case SPEED:
                    unit.setText(" km/h");
                    max = 25;
                    break;
            }
            initialize_picker();
            startListener();
            return v;
        }

        public void initialize_picker(){
            goal.setMaxValue(max);
            goal.setMinValue(0);
            goal.setValue(curBar.getMax());
        }

        public void startListener(){
            done.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    sp.edit().putInt(String.valueOf(type), goal.getValue()).apply();
                    parent.updateValue(parent.getView());
                    parent.getFragmentManager().beginTransaction().remove(cur).commit();
                }
            });
        }
    }
}