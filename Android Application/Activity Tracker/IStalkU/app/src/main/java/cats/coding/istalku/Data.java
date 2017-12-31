package cats.coding.istalku;

/**
 * Created by sungeee on 11/18/17.
 */

public class Data {
    String timestamp;
    String lat;
    String lng;

    public Data(String timestamp, String lat, String lng) {
        this.timestamp = timestamp;
        this.lat = lat;
        this.lng = lng;
    }

    public String getTime(){
        return timestamp;
    }

    public String getLat(){
        return lat;
    }

    public String getLng(){ return lng; }
}
