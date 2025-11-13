using UnityEngine;

public class SnapZone : MonoBehaviour
{
    public Color acceptedColor;
    public Transform snapPoint;

    private void OnTriggerEnter(Collider other)
    {
        // Vérifie que l’objet a bien un GrabbableBehavior
        GrabbableBehavior grabbable = other.GetComponent<GrabbableBehavior>();
        if (!grabbable) return;

        // Vérifie que l'objet n'est pas tenu
        if (grabbable.IsHeld()) return;

        Renderer rend = other.GetComponent<Renderer>();
        if (rend == null) return;

        Color objectColor = rend.material.color;

        // Snap uniquement si la couleur correspond ET que l'objet n'est pas tenu
        if (ApproximatelyEqualColor(objectColor, acceptedColor))
        {
            Rigidbody rb = other.GetComponent<Rigidbody>();
            if (rb)
            {
                rb.isKinematic = true;
                rb.useGravity = false;
            }

            other.transform.position = snapPoint.position;
            other.transform.rotation = snapPoint.rotation;

            Debug.Log("✅ Snap réussi !");
        }
        else
        {
            Debug.Log("❌ Mauvaise couleur, pas de snap.");
        }
    }

    private bool ApproximatelyEqualColor(Color a, Color b, float tolerance = 0.1f)
    {
        return Mathf.Abs(a.r - b.r) < tolerance &&
               Mathf.Abs(a.g - b.g) < tolerance &&
               Mathf.Abs(a.b - b.b) < tolerance;
    }
}
