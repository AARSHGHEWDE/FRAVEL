import { UtensilsCrossed, Star, MapPin } from "lucide-react";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import type { RestaurantOption } from "../../types";

export default function RestaurantCard({ restaurant }: { restaurant: RestaurantOption }) {
  return (
    <Card hover className="flex gap-4">
      {restaurant.image_url ? (
        <img
          src={restaurant.image_url}
          alt={restaurant.name}
          className="h-24 w-24 rounded-xl object-cover"
        />
      ) : (
        <div className="flex h-24 w-24 items-center justify-center rounded-xl bg-amber-100 dark:bg-amber-900/30">
          <UtensilsCrossed size={32} className="text-amber-600" />
        </div>
      )}
      <div className="flex-1 space-y-1">
        <h4 className="font-semibold">{restaurant.name}</h4>
        <div className="flex items-center gap-2">
          <Badge variant="warning">{restaurant.cuisine}</Badge>
          <span className="flex items-center gap-1 text-sm text-amber-500">
            <Star size={14} fill="currentColor" /> {restaurant.rating}
          </span>
          <span className="text-sm text-surface-400">
            {"$".repeat(restaurant.price_level)}
          </span>
        </div>
        <p className="flex items-center gap-1 text-xs text-surface-400">
          <MapPin size={12} /> {restaurant.address}
        </p>
      </div>
    </Card>
  );
}
